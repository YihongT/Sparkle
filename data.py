import json
import multiprocessing
import os
import random
from multiprocessing import Manager, Pool

from prompts.data import SHORTEST_QUESTION_TEMPLATES, TSP_QUESTION_TEMPLATES
from utils.args_utils import get_args
from utils.data_utils import (
    SpatialRelationshipMCQGenerator,
    describe_spatial_relationships,
    describe_spatial_relationships_new,
    generate_hop_pairs,
    generate_shortest_data_worker,
    generate_static_data_worker,
    generate_tsp_data_worker,
)
from utils.io_utils import load_json


def format_tsp_question(template, value):
    objects = value['colors']
    permutation = value['permutation']
    start_object = objects[permutation[0]]
    objects_string = '\n'.join(f'- {obj}' for obj in objects)

    return template.format(
        num_objects=len(objects),
        objects_string=objects_string,
        start_color=start_object,
        objects=json.dumps(objects, ensure_ascii=False),
    )


def get_tsp_question_templates(tsp_type):
    if tsp_type == 'fixstart':
        return [template for template in TSP_QUESTION_TEMPLATES if '{start_color}' in template]
    if tsp_type == 'free':
        return [template for template in TSP_QUESTION_TEMPLATES if '{start_color}' not in template]
    raise ValueError("Invalid tsp_type")


def generate_static_data(args, num_workers=4):
    multiprocessing.set_start_method('spawn')

    def generate_subset(data_type, num_items):
        manager = Manager()
        results = manager.list()

        with Pool(num_workers) as pool:
            i = 0
            while i < num_items:
                result = pool.apply_async(generate_static_data_worker, (args, i, data_type))
                res = result.get()
                if res:
                    results.append(res)
                    i += 1
        
        all_infos = {res['index']: res for res in results}

        if data_type == 'train':
            with open(f'{args.data_dir}/{args.train_folder}/{data_type}_info.json', 'w', encoding='utf-8') as f:
                json.dump(all_infos, f, ensure_ascii=False, indent=4)
        
        else:
            with open(f'{args.data_dir}/{args.test_folder}/{data_type}_info.json', 'w', encoding='utf-8') as f:
                json.dump(all_infos, f, ensure_ascii=False, indent=4)
        
        return all_infos

    if args.num_train > 0:
        os.makedirs(f'{args.data_dir}/{args.train_folder}/imgs', exist_ok=True)
                
        png_files = [f for f in os.listdir(f'{args.data_dir}/{args.train_folder}/imgs') if f.endswith('.png')]
        if os.path.exists(f'{args.data_dir}/{args.train_folder}/train_info.json') and len(png_files) == args.num_train:
            print(f"Data already exists for {args.train_folder}")
            return

        generate_subset('train', args.num_train)
        
        if len(os.listdir(f'{args.data_dir}/{args.train_folder}/imgs')) == 0:
            os.rmdir(f'{args.data_dir}/{args.train_folder}/imgs')
        
    if args.num_test > 0:
        os.makedirs(f'{args.data_dir}/{args.test_folder}/imgs', exist_ok=True)

        png_files = [f for f in os.listdir(f'{args.data_dir}/{args.test_folder}/imgs') if f.endswith('.png')]
        if os.path.exists(f'{args.data_dir}/{args.test_folder}/test_info.json') and len(png_files) == args.num_test:
            print(f"Data already exists for {args.test_folder}")
            return
        
        generate_subset('test', args.num_test)
        
        if len(os.listdir(f'{args.data_dir}/{args.test_folder}/imgs')) == 0:
            os.rmdir(f'{args.data_dir}/{args.test_folder}/imgs')
        

def generate_static_qa(args):
    if args.num_train > 0:
        if os.path.exists(f'{args.data_dir}/{args.train_folder}/train.jsonl'):
            print(f"QA data already exists for {args.train_folder}")
            return
        data_dir = f'{args.data_dir}/{args.train_folder}'
        train_info = load_json(f'{data_dir}/train_info.json')
        img_dir = f"{args.data_dir}/{args.train_folder}/imgs/"

        train_set = []
        train_dir_set, train_dis_set, train_pos_set = [], [], []
        for index, dict_value in train_info.items():
            query, answer, direction_query, direction_answer, distance_query, distance_answer, position_query, position_answer = describe_spatial_relationships(dict_value, abs=args.abs)
            train_query_list, train_answer_list, train_dir_query_list, train_dir_resp_list, train_dis_query_list, train_dis_resp_list, train_pos_query_list, train_pos_resp_list,  = describe_spatial_relationships_new(dict_value, abs=args.abs)
            img_path = f"{img_dir}train_{index}.png"
            
            for train_query, train_answer in zip(train_query_list, train_answer_list):
                train_set.append({'query': train_query, 'response': train_answer, 'images': [img_path]})
            for train_query, train_answer in zip(train_dir_query_list, train_dir_resp_list):
                train_dir_set.append({'query': train_query, 'response': train_answer, 'images': [img_path]})
            for train_query, train_answer in zip(train_dis_query_list, train_dis_resp_list):
                train_dis_set.append({'query': train_query, 'response': train_answer, 'images': [img_path]})
            for train_query, train_answer in zip(train_pos_query_list, train_pos_resp_list):
                train_pos_set.append({'query': train_query, 'response': train_answer, 'images': [img_path]})
        
            train_set.append({'query': query, 'response': answer, 'images': [img_path]})
            train_dir_set.append({'query': direction_query, 'response': direction_answer, 'images': [img_path]})
            train_dis_set.append({'query': distance_query, 'response': distance_answer, 'images': [img_path]})
            train_pos_set.append({'query': position_query, 'response': position_answer, 'images': [img_path]})
            
        random.shuffle(train_set)
        random.shuffle(train_dir_set)
        random.shuffle(train_dis_set)
        random.shuffle(train_pos_set)
        
        with open(f'{args.data_dir}/{args.train_folder}/train_full.jsonl', 'w') as f:
            for item in train_set:
                json_line = json.dumps(item)
                f.write(json_line + '\n')
        
        with open(f'{args.data_dir}/{args.train_folder}/train_direction.jsonl', 'w') as f:
            for item in train_dir_set:
                json_line = json.dumps(item)
                f.write(json_line + '\n')
                
                
        with open(f'{args.data_dir}/{args.train_folder}/train_distance.jsonl', 'w') as f:
            for item in train_dis_set:
                json_line = json.dumps(item)
                f.write(json_line + '\n')
                
                
        with open(f'{args.data_dir}/{args.train_folder}/train_position.jsonl', 'w') as f:
            for item in train_pos_set:
                json_line = json.dumps(item)
                f.write(json_line + '\n')

    if args.num_test > 0:
        if os.path.exists(f'{args.data_dir}/{args.test_folder}/test.json'):
            print(f"QA data already exists for {args.test_folder}")
            return
        data_dir = f'{args.data_dir}/{args.test_folder}'
        test_info = load_json(f'{data_dir}/test_info.json')
        img_dir = f"{args.data_dir}/{args.test_folder}/imgs/"

        test_set = {}
        for index, dict_value in test_info.items():
            generator = SpatialRelationshipMCQGenerator(dict_value, num_directions=args.num_direction)
            distance_question, distance_answer = generator.generate_distance_question()
            direction_question, direction_answer = generator.generate_direction_question()
            position_question, position_answer = generator.generate_position_question()

            test_set[index] = {
                'distance': {'question': distance_question, 'answer': distance_answer},
                'direction': {'question': direction_question, 'answer': direction_answer},
                'position': {'question': position_question, 'answer': position_answer}
            }
            
        with open(f'{args.data_dir}/{args.test_folder}/test.json', 'w', encoding='utf-8') as f:
            json.dump(test_set, f, ensure_ascii=False, indent=4)    


def generate_tsp_data(args):
    multiprocessing.set_start_method('spawn')

    def generate_subset(data_type, num_items):
        manager = Manager()
        results = manager.list()

        with Pool(4) as pool:
            i = 0
            while i < num_items:
                result = pool.apply_async(generate_tsp_data_worker, (args, i, data_type))
                res = result.get()
                if res:
                    results.append(res)
                    i += 1
        
        all_infos = {res['index']: res for res in results}

        if data_type == 'train':
            with open(f'{args.data_dir}/{args.train_folder}/{data_type}_info.json', 'w', encoding='utf-8') as f:
                json.dump(all_infos, f, ensure_ascii=False, indent=4)
        
        else:
            with open(f'{args.data_dir}/{args.test_folder}/{data_type}_info.json', 'w', encoding='utf-8') as f:
                json.dump(all_infos, f, ensure_ascii=False, indent=4)
        
        return all_infos

    if args.num_train > 0:
        os.makedirs(f'{args.data_dir}/{args.train_folder}/imgs', exist_ok=True)

        png_files = [f for f in os.listdir(f'{args.data_dir}/{args.train_folder}/imgs') if f.endswith('.png')]
        if os.path.exists(f'{args.data_dir}/{args.train_folder}/train_info.json') and len(png_files) == args.num_train:
            print(f"Data already exists for {args.train_folder}")
            return
        generate_subset('train', args.num_train)
        
        if len(os.listdir(f'{args.data_dir}/{args.train_folder}/imgs')) == 0:
            os.rmdir(f'{args.data_dir}/{args.train_folder}/imgs')
        
    if args.num_test > 0:
        os.makedirs(f'{args.data_dir}/{args.test_folder}/imgs', exist_ok=True)

        png_files = [f for f in os.listdir(f'{args.data_dir}/{args.test_folder}/imgs') if f.endswith('.png')]
        if os.path.exists(f'{args.data_dir}/{args.test_folder}/test_info.json') and len(png_files) == args.num_test:
            print(f"Data already exists for {args.test_folder}")
            return

        generate_subset('test', args.num_test)
        
        if len(os.listdir(f'{args.data_dir}/{args.test_folder}/imgs')) == 0:
            os.rmdir(f'{args.data_dir}/{args.test_folder}/imgs')
        

def generate_tsp_qa(args):
    if args.num_train > 0:
        raise NotImplementedError
    
    if args.num_test > 0:
        templates = get_tsp_question_templates(args.tsp_type)
        if os.path.exists(f'{args.data_dir}/{args.test_folder}/test.json'):
            existing_test = load_json(f'{args.data_dir}/{args.test_folder}/test.json')
            has_unformatted_template = any(
                '{objects_string}' in sample.get('question', '') or '{num_objects}' in sample.get('question', '')
                for sample in existing_test.values()
            )
            if args.tsp_type == 'fixstart':
                has_wrong_prompt_type = any('Starts at the ' not in sample.get('question', '') for sample in existing_test.values())
            else:
                has_wrong_prompt_type = any('Starts at the ' in sample.get('question', '') for sample in existing_test.values())
            if not has_unformatted_template and not has_wrong_prompt_type:
                print(f"QA data already exists for {args.test_folder}")
                return
            print(f"Regenerating stale QA data for {args.test_folder}")
        data_dir = f'{args.data_dir}/{args.test_folder}'
        test_info = load_json(f'{data_dir}/test_info.json')
        
        tsp_qa = {}
        for key, value in test_info.items():
            gt = [value['colors'][idx] for idx in value['permutation']]            
            question = format_tsp_question(random.choice(templates), value)
            tsp_qa[key] = {'question': question, 'answer': gt}
            
        with open(f'{args.data_dir}/{args.test_folder}/test.json', 'w', encoding='utf-8') as f:
            json.dump(tsp_qa, f, ensure_ascii=False, indent=4)    


def generate_shortest_data(args):
    multiprocessing.set_start_method('spawn')

    def generate_subset(data_type, num_items, start_end_pairs):
        manager = Manager()
        results = manager.list()

        with Pool(4) as pool:
            i = 0
            while i < num_items:
                result = pool.apply_async(generate_shortest_data_worker, (args, i, data_type, start_end_pairs[i]))
                res = result.get()
                if res:
                    results.append(res)
                    i += 1
        
        all_infos = {res['index']: res for res in results}

        if data_type == 'train':
            with open(f'{args.data_dir}/{args.train_folder}/{data_type}_info.json', 'w', encoding='utf-8') as f:
                json.dump(all_infos, f, ensure_ascii=False, indent=4)
        
        else:
            with open(f'{args.data_dir}/{args.test_folder}/{data_type}_info.json', 'w', encoding='utf-8') as f:
                json.dump(all_infos, f, ensure_ascii=False, indent=4)
        
        return all_infos

    if args.num_train > 0:
        os.makedirs(f'{args.data_dir}/{args.train_folder}/imgs', exist_ok=True)

        start_end_pairs = generate_hop_pairs(n=args.ngrid, m=args.num_train, k=args.min_hops)
        assert len(start_end_pairs) == args.num_train

        png_files = [f for f in os.listdir(f'{args.data_dir}/{args.train_folder}/imgs') if f.endswith('.png')]
        if os.path.exists(f'{args.data_dir}/{args.train_folder}/train_info.json') and len(png_files) == args.num_train:
            print(f"Data already exists for {args.train_folder}")
            return

        generate_subset('train', args.num_train, start_end_pairs)
        
        if len(os.listdir(f'{args.data_dir}/{args.train_folder}/imgs')) == 0:
            os.rmdir(f'{args.data_dir}/{args.train_folder}/imgs')
        
    if args.num_test > 0:
        os.makedirs(f'{args.data_dir}/{args.test_folder}/imgs', exist_ok=True)

        start_end_pairs = generate_hop_pairs(n=args.ngrid, m=args.num_test, k=args.min_hops)
        assert len(start_end_pairs) == args.num_test

        png_files = [f for f in os.listdir(f'{args.data_dir}/{args.test_folder}/imgs') if f.endswith('.png')]
        if os.path.exists(f'{args.data_dir}/{args.test_folder}/test_info.json') and len(png_files) == args.num_test:
            print(f"Data already exists for {args.test_folder}")
            return

        generate_subset('test', args.num_test, start_end_pairs)
        
        if len(os.listdir(f'{args.data_dir}/{args.test_folder}/imgs')) == 0:
            os.rmdir(f'{args.data_dir}/{args.test_folder}/imgs')
        

def generate_shortest_qa(args):
    if args.num_train > 0:
        raise NotImplementedError
    
    if args.num_test > 0:
        if os.path.exists(f'{args.data_dir}/{args.test_folder}/test.json'):
            print(f"QA data already exists for {args.test_folder}")
            return
        data_dir = f'{args.data_dir}/{args.test_folder}'
        test_info = load_json(f'{data_dir}/test_info.json')
        
        shortest_qa = {}
        for key, value in test_info.items():
            gt_shortest_path_length = value['gt_shortest_path_length']
            question = SHORTEST_QUESTION_TEMPLATES[0]
            shortest_qa[key] = {'question': question, 'answer': gt_shortest_path_length}
            
        with open(f'{args.data_dir}/{args.test_folder}/test.json', 'w', encoding='utf-8') as f:
            json.dump(shortest_qa, f, ensure_ascii=False, indent=4)    



if __name__ == "__main__":
    args = get_args()
    if args.run_type == 'static':
        generate_static_data(args)
        generate_static_qa(args)
        
    elif args.run_type == 'tsp':
        generate_tsp_data(args)
        generate_tsp_qa(args)
        
    elif args.run_type == 'shortest':
        generate_shortest_data(args)
        generate_shortest_qa(args) 
    else:
        raise ValueError
