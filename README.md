## Prequisites

1. Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows)
2. Install [ScreenStream](https://github.com/dkrivoruchko/ScreenStream) on your Android for screen capture
3. Install [geckodriver](https://github.com/mozilla/geckodriver/releases) to open Firefoxx
4. Run this to install all the packages required:

```
pip install -r requirements.txt
```



## Usage

1. Open `cmd` in this folder or `cd` here
2. Import
```
import gbot
```
3. Open Firefox
```
gbot.start('cft', 100) # cft for confetti, 100 in 192.168.1.100
```
4. Run:
```
gbot.run() # capture from phone -> ocr -> search
```

```
gbot.run_history('m-dd', 1) # file from m-dd -> ocr -> search
```