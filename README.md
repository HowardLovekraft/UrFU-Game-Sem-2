# Описание игры
Слепой человек хочет дойти от дома до поликлиники.    
Из-за невозможности ориентироваться, полагаясь на зрение,
игроку придётся полагаться на слух главного героя и трость.

# Как установить игру
## Через [`uv`](https://github.com/astral-sh/uv) (не зависит от ОС):
1. Скачайте репозиторий:  
`git clone https://github.com/HowardLovekraft/UrFU-Game-Sem-2`
2. Установите виртуальное окружение (в директории репозитория "UrFU-Game-Sem-2/"):  
`uv venv`
3. Запустите игру:  
`uv run src/game.py`  
Менеджер зависимостей самостоятельно установит необходимые пакеты в виртуальное окружение.

## Через `venv`
### Windows
1. Скачайте репозиторий:  
`git clone https://github.com/HowardLovekraft/UrFU-Game-Sem-2`

2. Установите виртуальное окружение (в директории скачанного репозитория):  
	`python3 -m venv venv`
	
3. Активируйте виртуальное окружение:  
	`venv/Scripts/activate.bat`

4. Установите зависимости:  
	`pip install -r requirements.txt`

5. Запустите игру:  
	`python3 src/game.py`

### Linux/MacOS
1. Скачайте репозиторий:  
`git clone https://github.com/HowardLovekraft/UrFU-Game-Sem-2`

 2. Установите виртуальное окружение (в директории скачанного репозитория):  
	`pytnon -m venv venv`

3. Активируйте виртуальное окружение:  
	`source venv/bin/activate`

4. Установите зависимости:  
	`pip install -r requirements.txt`

5. Запустите игру:  
	`python src/game.py`