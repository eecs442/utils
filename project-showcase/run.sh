WEBSITE_DIR=/Users/jcjohns/code/eecs442/website/

REMOTE_HOST=web.eecs.umich.edu
REMOTE_USER=justincj
REMOTE_HOME=/w/web/u/j/justincj
REMOTE_DIR=$REMOTE_HOME/public_html/teaching/eecs442/projects/WI2021

python parse_wi2021.py

# `python make_previews.py \
# `  --input-dir WI2021/public_pdfs \
# `  --output-dir WI2021/public_imgs
# ` 
# `python make_previews.py \
# `  --input-dir WI2021/course_pdfs \
# `  --output-dir WI2021/course_imgs

cp WI2021/public.yaml $WEBSITE_DIR/_data/projects_WI2021.yaml
rsync -r WI2021/public_pdfs $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/pdfs
rsync -r WI2021/public_imgs $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/imgs
