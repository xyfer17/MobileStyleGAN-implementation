import argparse
import os
import cv2
import torch
import numpy as np
from core.utils import load_cfg, load_weights, tensor_to_img
from core.distiller import Distiller
from core.model_zoo import model_zoo


def main(args):
    cfg = load_cfg(args.cfg)
    distiller = Distiller(cfg)
    if args.ckpt is not None:
        ckpt = model_zoo(args.ckpt)
        load_weights(distiller, ckpt["state_dict"])

    for i in range(args.n_output):
        var = torch.randn(1, distiller.mapping_net.style_dim)
        img_s = distiller(var, truncated=args.truncated)
        path = args.output_path+"pic"+str(i)+".jpg"
        cv2.imwrite(path, tensor_to_img(img_s[0].cpu()))
        key = chr(cv2.waitKey() & 255)
        if key == 'q':
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # pipeline configure
    parser.add_argument("--cfg", type=str, default="configs/mobile_stylegan_ffhq.json", help="path to config file")
    parser.add_argument("--ckpt", type=str, default="mobilestylegan_ffhq.ckpt", help="path to checkpoint")
    parser.add_argument("--output-path", type=str, default="./", help="path to store images")
    parser.add_argument("--n-output", type=int, default=50, help="number of batches")
    parser.add_argument("--truncated", action='store_true', help="use truncation mode")
    
    args = parser.parse_args()
    main(args)
