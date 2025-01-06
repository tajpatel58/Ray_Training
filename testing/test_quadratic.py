from ..math_funcs.quadratic import quadratic_curve
from pathlib import Path
import random
import numpy as np
import ray


def generate_y_coordinates(a: float, 
                           b: float,
                           c: float, 
                           x_coords: list,
                           use_ray: bool) -> list:
    if use_ray:
        wheel_path = Path(__file__).resolve().parent / "dist" / "tp_math-0.1.0-py3-none-any.whl"
        print(wheel_path)
        ray.init(ignore_reinit_error=True,
                 runtime_env={"py_modules" : [str(wheel_path)]})
        
        @ray.remote
        def quadratic_curve_ray(x: float) -> float:
            return quadratic_curve(a, b, c, x)
        

        tasks = [quadratic_curve_ray.remote(x_i) for x_i in x_coords]
        results = ray.get(tasks)
        ray.shutdown()
        return results

    else:
        return [quadratic_curve(a, b, c, x_i) for x_i in x_coords]
