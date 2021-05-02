import argparse
import os
import tempfile
import shutil
import imageio
import numpy as np
import PIL


parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', default='sample_data/pdfs')
parser.add_argument('--output-dir', default='sample_data/imgs')

parser.add_argument('--pages', type=int, default=5)
parser.add_argument('--height', type=int, default=800)
parser.add_argument('--border', type=int, default=2)

parser.add_argument('--density', type=int, default=300)
parser.add_argument('--resize', type=int, default=50)


def resize_image(img, height):
  H, W = img.shape[0], img.shape[1]
  s = height / H
  HH = height
  WW = int(round(s * W))
  img = np.array(PIL.Image.fromarray(img).resize((WW, HH)))
  return img


def handle_file(args, in_path, out_path):  
  width = None

  temp_dir = tempfile.mkdtemp()
  temp_path = os.path.join(temp_dir, 'page-%03d.png')

  # Use ImageMagick to convert PDF input into a a set of PNGs (one per page)
  cmd = ' '.join([
    f'convert',
    f'-density {args.density}',
    f'{in_path}',
    f'-background white',
    f'-alpha Remove',
    f'-resize {args.resize}%',
    f'-colorspace RGB',
    f'-depth 8',
    f'{temp_path}',
  ])
  print(cmd)
  os.system(cmd)

  page_paths = sorted(os.listdir(temp_dir))
  page_imgs = []
  for i in range(args.pages):
    if i >= len(page_paths):
      page_img = np.empty((args.height, width, 3), dtype=np.uint8)
      page_img[:] = 255
      page_imgs.append(page_img)
      continue
    page_path = os.path.join(temp_dir, page_paths[i])
    page_img = imageio.imread(page_path)
    if page_img.ndim == 2:
      page_img = np.repeat(page_img[:, :, None], 3, axis=2)
    page_img = resize_image(page_img, args.height)
    width = page_img.shape[1]
    p = args.border
    page_img[:p] = 0     # Top border
    page_img[-p:] = 0    # Bottom border
    p_left = 2 * p if i == 0 else p
    p_right = 2 * p if i + 1 == args.pages else p
    page_img[:, :p_left] = 0   # Left border
    page_img[:, -p_right:] = 0  # Right border
    page_imgs.append(page_img)
  
  preview_img = np.hstack(page_imgs)
  imageio.imsave(out_path, preview_img)

  shutil.rmtree(temp_dir)


def main(args):
  for fn in os.listdir(args.input_dir):
    name, ext = os.path.splitext(fn)
    in_path = os.path.join(args.input_dir, fn)
    out_path = os.path.join(args.output_dir, f'{name}.png')
    handle_file(args, in_path, out_path)


if __name__ == '__main__':
  main(parser.parse_args())
