import os
import argparse
from utils.base_utils import seed_everything


def get_args():

    parser = argparse.ArgumentParser(description='Generate spatial reasoning datasets.')

    # process settings
    parser.add_argument('--seed', type=int, default=0, help='Seed everything')
    # io settings
    parser.add_argument('--data_dir', type=str, default='./data', help='')
    parser.add_argument('--folder', type=str, default='', help='custom subfolder for auxiliary scripts')
    # run settings
    parser.add_argument('--run_type', type=str, choices=['static', 'tsp', 'shortest'], default='static', help='')

    # data settings
    parser.add_argument('--num_direction', type=int, choices=[4, 8], default=8, help='')
    parser.add_argument('--num_basic_points', type=int, default=3, help='')
    parser.add_argument('--num_noise_points', type=int, default=2, help='')
    parser.add_argument('--textobj', action='store_true', default=False, help='display text on objects of the static image')
    parser.add_argument('--abs', action='store_true', default=False, help='add absolute training')
    parser.add_argument('--tsp_type', type=str, choices=['free', 'fixstart'], default='fixstart', help='')
    parser.add_argument('--obj_color', type=str, default='lightgray', help='')
    parser.add_argument('--font_color', type=str, default='black', help='')
    parser.add_argument('--ngrid', type=int, default=5, help='')
    parser.add_argument('--textgrid', action='store_true', default=False, help='display text on nodes of the grid graph')
    parser.add_argument('--min_hops', type=int, default=2, help='')
    parser.add_argument('--radius', type=float, default=0.05, help='')
    parser.add_argument('--img_width', type=int, default=10, help='width and height of imgs')
    parser.add_argument('--distance_threshold', type=float, default=0.2, help='To ensure objects are visually separated')
    parser.add_argument('--num_train', type=int, default=0, help='')
    parser.add_argument('--num_test', type=int, default=0, help='')

    args = parser.parse_args()

    # assert (args.num_train != 0 and args.num_test == 0) or (args.num_train == 0 and args.num_test != 0)
    if not ((args.num_train != 0 and args.num_test == 0) or (args.num_train == 0 and args.num_test != 0)):
        raise ValueError("Invalid configuration: Either `num_train` should be non-zero and `num_test` should be zero, or `num_train` should be zero and `num_test` should be non-zero.")

    
    seed_everything(args.seed)
        
    args.data_dir = f'{args.data_dir}/{args.run_type}'
    
    if args.run_type == 'static':
        args.train_folder = f"train{args.num_train}_textobj{args.textobj}_basic{args.num_basic_points}_noise{args.num_noise_points}_threshold{args.distance_threshold}_directions{args.num_direction}_abs{args.abs}"
        args.test_folder = f"test{args.num_test}_textobj{args.textobj}_basic{args.num_basic_points}_noise{args.num_noise_points}_threshold{args.distance_threshold}_directions{args.num_direction}"
    
    elif args.run_type == 'tsp':
        args.train_folder = f"train{args.num_train}_textobj{args.textobj}_point{args.num_basic_points}_threshold{args.distance_threshold}_{args.tsp_type}"
        args.test_folder = f"test{args.num_test}_textobj{args.textobj}_point{args.num_basic_points}_threshold{args.distance_threshold}_{args.tsp_type}"
    
    elif args.run_type == 'shortest':
        args.train_folder = f"train{args.num_train}_grid{args.ngrid}_text{args.textgrid}_min_hops{args.min_hops}"
        args.test_folder = f"test{args.num_test}_grid{args.ngrid}_text{args.textgrid}_min_hops{args.min_hops}"
    
    else:
        raise ValueError
    
    
    if args.num_train > 0:
        if not os.path.exists(f'{args.data_dir}/{args.train_folder}'):
            os.makedirs(f'{args.data_dir}/{args.train_folder}', exist_ok=True)
    else:
        if not os.path.exists(f'{args.data_dir}/{args.test_folder}'):
            os.makedirs(f'{args.data_dir}/{args.test_folder}', exist_ok=True)

    return args


if __name__ == '__main__':
    # args = get_args()
    pass
    
