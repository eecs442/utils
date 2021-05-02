import argparse
import yaml


SAMPLE_PATH = '../../website/_data/projects_sample.yaml'


def main():
  with open(SAMPLE_PATH, 'r') as f:
    data = yaml.safe_load(f)
  
  base_url = data['base_url']
  for project in data['projects']:
    _id = project['id']
    img_url = f'{base_url}/imgs/{_id}.png'
    pdf_url = f'{base_url}/pdfs/{_id}.pdf'
    title = project['title']
    authors = ', '.join(project['authors'])
    print(f'<a href="{pdf_url}"><h2>{title}</h2></a>')
    print(f'<h3>{authors}</h3>')
    print(f'<a href="{pdf_url}"><img src="{img_url}" style="width:100%"></a>')




if __name__ == '__main__':
  main()

