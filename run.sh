#!/usr/bin/env bash

# Examples (pick one and adjust parameters as needed):
# python -u data.py --run_type static --num_train 1000 --num_basic_points 3 --num_noise_points 2 --num_direction 8 --textobj --abs
python -u data.py --run_type static --num_test 20 --num_basic_points 3 --num_noise_points 2 --num_direction 8 --textobj
python -u data.py --run_type shortest --num_test 20 --ngrid 5 --textgrid
python -u data.py --run_type tsp --num_test 20 --num_basic_points 5 --textobj
