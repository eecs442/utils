import argparse
import csv
import os
import yaml
import shutil
from collections import Counter


parser = argparse.ArgumentParser()
parser.add_argument('--projects_csv', default='WI2021/projects.csv')
parser.add_argument('--showcase_csv', default='WI2021/showcase.csv')

parser.add_argument('--all_pdf_dir', default='WI2021/all_pdfs')
parser.add_argument('--public_pdf_dir', default='WI2021/public_pdfs')
parser.add_argument('--course_pdf_dir', default='WI2021/course_pdfs')
parser.add_argument('--public_yaml_path', default='WI2021/public.yaml')
parser.add_argument('--course_yaml_path', default='WI2021/course.yaml')
parser.add_argument('--base_url', default='https://web.eecs.umich.edu/~justincj/teaching/eecs442/projects/WI2021')


overrides = {
  'xun fu': 'ykgong',
  'rkrawec': 'ahreehong',
  'doredlaj': 'doredla',
}


def main(args):
  projects = {}
  with open(args.projects_csv, 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
      if i == 0:
        continue
      project_id = row[0]
      if project_id == '':
        continue
      project_id = f'{int(project_id):03}'
      authors = row[1].split(', ')
      filename = row[2]
      if not authors[0]:
        continue
      projects[filename] = {
        'id': project_id,
        'authors': authors,
        'filename': filename,
        'acl': None,
        'title': None,
      }

  with open(args.showcase_csv, 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
      if i == 0:
        continue
      title = row[2]
      raw_acl = row[3]
      acl = None
      if raw_acl == 'Publicly visible to anyone on the course website':
        acl = 'public'
      elif raw_acl == 'Visible to the course staff only':
        acl = 'private'
      elif raw_acl == 'Visible to students enrolled in EECS 442 this semester':
        acl = 'course'
      assert acl is not None, raw_acl
      project = None
      for j in range(5):
        uniqname = row[4 + j].lower().strip()
        uniqname = overrides.get(uniqname, uniqname)
        if uniqname == '':
          continue
        project = projects.get(uniqname, None)
        if project is not None:
          break
      if project is None:
        print('Could not find match for showcase project with authors:')
        print(row[4:9])
      project['acl'] = acl
      project['title'] = title

  projects_by_acl = {}
  for acl in ['public', 'course', 'private']:
    filtered = [p for p in projects.values() if p['acl'] == acl]
    projects_by_acl[acl] = filtered
    print(acl, len(filtered))

  handle_project_set(
      projects_by_acl['public'],
      args,
      args.public_pdf_dir,
      args.public_yaml_path)
  handle_project_set(
      projects_by_acl['public'] + projects_by_acl['course'],
      args,
      args.course_pdf_dir,
      args.course_yaml_path)


def handle_project_set(projects, args, pdf_dir, yaml_path):
  if not os.path.isdir(pdf_dir):
    os.makedirs(pdf_dir)

  project_data = {
    'base_url': args.base_url,
    'projects': [],
  }
  for project in projects:
    project_data['projects'].append({
      'id': project['id'],
      'title': project['title'],
      'authors': [a for a in project['authors']],
    })

  with open(yaml_path, 'w') as f:
    yaml.safe_dump(project_data, f)

  for project in projects:
    filename = project['filename']
    project_id = project['id']
    src_pdf_path = f'{args.all_pdf_dir}/{filename}.pdf'
    tgt_pdf_path = f'{pdf_dir}/{project_id}.pdf'
    shutil.copy(src_pdf_path, tgt_pdf_path)
  


if __name__ == '__main__':
  main(parser.parse_args())
