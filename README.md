# TeamProject - Steam Game Recommender
아주대학교 23-02 데이터마이닝 팀프로젝트 : 스팀 게임 추천

## Contents
+ [Project Goal](#project-goal)
+ [Tech Stacks](#tech-stacks)
+ [Dataset Description](#dataset-description)
+ [Code Description](#code-description)
+ [Project Result](#project-result)
+ [Team members](#team-members)

## :bulb: Project Goal  
현재 Steam 플랫폼은 전 세계적으로 수백만 명의 사용자를 보유하고 있으며, 수 많은 게임을 제공하고 있습니다. 현재(2023.12) 7만여 개의 게임이 등록되어 있으며, 2023년 한 해에만 약 11000여 개의 게임이 새로 등록된 상황입니다. 이러한 다양성은 사용자에게 다양한 선택의 폭을 제공하지만, 동시에 사용자가 흥미를 느낄만한 적합한 게임을 찾기 어렵게 만듭니다. 또한 Steam 플랫폼은 웹사이트에 사용자 ID만 표시하기 때문에 사용자가 다른 사용자의 특성을 파악하기 어려워 사람들 간의 의사소통이 어렵습니다.

이 프로젝트의 목적은 Steam 사용자에게 개인화된 게임 추천을 제공하는 것 뿐만 아니라 사용자가 가지고 있는 몇 가지 특성을 태그화하여 이러한 문제를 해결하는 것입니다. 이는 사용자의 게임 경험을 향상시키고 커뮤니티로서의 플랫폼의 활용도를 높일 수 있는 중요한 접근 방식입니다. 본 프로젝트의 결과를 통해 Steam 게임 추천 시스템의 효과를 높이는 방법을 찾고 Steam 웹사이트의 커뮤니티로서의 사용자 만족도 향상에 도움을 주고자 합니다. 이번 프로젝트의 최종 목표는 게임 선택 과정을 보다 쉽게 하고 세부적인 사용자 태그 카테고리를 만드는 것이며, 또한 이를 통해 23-02 데이터마이닝 수업 과정에서 학습한 내용에 대한 이해를 높이는 것입니다.

## :wrench: Tech Stacks
### Environment
+ Google Colab  
+ Local Python
+ Steam Web API
### Development   
+ Python 3
+ NumPy
+ Pandas
+ SciPy
+ PySpark
+ urllib

## :bookmark_tabs: Dataset Description
일부 데이터셋은 개인을 특정할 수 있는 사용자 정보를 포함하여 Github에 업로드 하지 않습니다.
### [Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)
+ Kaggle에 등록되어 있는 데이터셋으로 이번 프로젝트에서는 AppID-Name 매핑 과정에 사용됨
### User-Games Dataset
+ Steam Web API를 통해 크롤링하여 직접 구축한 데이터셋
+ 전처리 전 30000여 명의 사용자 / 전처리 이후 4411명의 유효 사용자(친구 목록 및 게임 목록 공개)
+ Columns : Steam User64ID / 해당 사용자의 보유 게임 AppID / 해당 게임의 PlayTime
### Game-Feature Dataset
+ Steam Web API를 통해 크롤링하여 직접 구축한 데이터셋
+ Columns : Age(연령 등급) / is_Free(유무료 여부) / Genre(게임 장르)

## :open_file_folder: Repository Description
### Data Crawling & Preprocessing
데이터 크롤링은 그 양이 방대하여 각자 환경에 맞춰 코드 변형해 수행하였습니다.
+ [`ExtractData/...`](https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/tree/main/ExtractData) : UserList와 User-Games Data 추출 코드(정화식)
+ [`SteamCrawling/...`](https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/tree/main/SteamCrawling) : UserList와 User-Games Data 추출 코드(김태윤)
+ [`UserCrawler.ipynb`](https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/blob/main/UserCrawler.ipynb) : UserList 크롤링과 결과 종합 및 가공 코드(양성호)
+ [`UserOwnedGameCrawler.ipynb`](https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/blob/main/UserOwnedGameCrawler.ipynb) : User-Games Data 추출과 결과 종합 및 가공 코드(양성호)
### Clustering
+ [`Clustering/...`](https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/tree/main/Clustering) : Clustering 및 User Tagging System 관련 코드(정화식)
### Frequent Itemsets & Association Rules(FP-Growth)
+ [`FIAR - FP-Growth.ipynb`](https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/blob/main/FIAR%20-%20FP-Growth.ipynb) : Code for Frequent Itemsets & Association Rules with FP-Growth(양성호)
+ [`Ensemble - FP&Cluster.ipynb`](https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/blob/main/Ensemble%20-%20FP-Cluster.ipynb) : Code for recommender based on FP-Growth and Cluster(양성호)
### Item-based Collaborative Filtering
+ [`Item-based Collaborative Filtering.ipynb`](https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/blob/main/Item-based%20Collaborative%20Filtering.ipynb) : Item-based Collaborative Filtering 구현 코드(김태윤)
### Etc.
+ [`Lab/...`](https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/tree/main/Lab) : Folder contains code files written during study and test algorithms

## :trophy: Project Result
### Clustering
<img src="https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/assets/93295755/a9080aca-f832-4d5f-bdbf-1d474e86e265" width="320"/></br>
`클러스터링 결과`</br>  
<img src="https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/assets/93295755/89f9e4c4-8214-4847-8c6a-9630215d11ae" width="320"/></br>
`클러스터링 결과 시각화`</br>  
<img src="https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/assets/93295755/78c041fb-595a-4bd2-a4e0-59d9bda49ade" width="320"/></br>
`클러스터링 결과 기반 사용자 태깅`</br>  
### Association Rules(FP-Growth)  
<img src="https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/assets/93295755/35b49c31-a9a6-4408-8961-d214cf365a05" width="640"/></br>
`추천 결과 <UserID : 765611983****6237 / Cluster ID : 0>`</br>  
<img src="https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/assets/93295755/21940f64-89b1-42c9-b03b-e03dfe154ee2" width="640"/></br>
`추천 결과 <UserID : 765611981****0779 / Cluster ID : 1>`</br>  
<img src="https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/assets/93295755/b8d7856c-cc52-46eb-98f1-0393765dd599" width="640"/></br>
`추천 결과 <UserID : 765611980****8500 / Cluster ID : 4>`</br>  
### Item-based Collaborative Filtering
<img src="https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/assets/93295755/3f9e81c7-187f-44b7-bbf0-d30d7f879372" width="640"/></br>
`Item-based Collaborative Filtering의 Utility Matrix`</br>  
<img src="https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/assets/93295755/78747932-3cf8-4f08-a644-d07dae9a3570" width="320"/></br>
`<30 Day of Defeat> 게임 기준 추천 결과`</br>  
<img src="https://github.com/AU2302DM-TeamKYJ/TeamProject-SteamGameRecommander/assets/93295755/a1d297cc-4e6e-4b7f-bc15-0610598b175e" width="480"/></br>
`위 내용을 AppID-Name-Genre 매핑한 결과`</br>  

## :blush: Team members
### 김태윤
+ [@Chokoty](https://github.com/Chokoty)
+ 소프트웨어학과
+ Steam User Data 크롤링 진행
+ Item-based Collaborative Filtering 담당
### 양성호
+ [@SyingSHY](https://github.com/SyingSHY)
+ 소프트웨어학과
+ Steam User Data 크롤링 진행
+ Association Rules(FP-Growth) 담당
### 정화식
+ [@JeongHwaSik](https://github.com/JeongHwaSik)
+ 소프트웨어학과
+ Steam User Data 크롤링 진행
+ Clustering 담당
