import csv


def write_ids_to_csv(file_name, id_list):
  """
    주어진 ID 목록을 CSV 파일에 저장합니다.

    :param file_name: 저장할 파일 이름
    :param id_list: 저장할 스팀 ID 목록
    """
  with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["SteamID"])
    for steam_id in id_list:
      writer.writerow([steam_id])


def read_ids_from_csv(file_name):
  """
    CSV 파일로부터 스팀 ID 목록을 읽어서 반환합니다.

    :param file_name: 읽을 파일 이름
    :return: 스팀 ID 목록
    """
  id_list = []
  with open(file_name, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 헤더를 건너뛰기
    for row in reader:
      id_list.append(row[0])
  return id_list


def read_ids_from_csv_2(file_name):
  """
  파일에서 단일 행에 있는 쉼표로 구분된 Steam ID 목록을 읽어서 반환합니다.

  :param file_name: 읽을 파일 이름
  :return: Steam ID 목록
  """
  with open(file_name, 'r', encoding='utf-8') as file:
    # 파일의 첫 번째 행을 읽음
    line = file.readline()
    # 쉼표로 구분하여 Steam ID 목록을 얻음
    steam_ids = line.strip().split(',')
    # 빈 문자열 제거 (마지막 쉼표 뒤에 생길 수 있음)
    steam_ids = [id for id in steam_ids if id]
  return steam_ids
