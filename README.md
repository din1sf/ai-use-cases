# POC GenAI


## Setup
- Python (tested with 3.12)
- [OpenAI account](https://platform.openai.com/docs/overview)
- Python libraries (streamlit, pandas, openai) - check requirements.txt
```
$ pip install -r requirements.txt
```

## Streamlit app

How to run streamlit app

```
$ streamlit run app.py
```

## Usecase 1

![alt text](uc1-image1.png "Snapshot 1")

- Upload XLS file
- Input prompt (e: Help me with Test data for the Put-away into high racks for the Warehouse/Plant 3551 .)
- Click "Generate" button
- Wait form OpenAI process
- View result as json string

![alt text](uc1-image2.png "Snapshot 2")

## Uscase 2

![alt text](uc2-image1.png "Snapshot 1")

- Upload image file
- Click "Process Image" button
- Wait for OpenAI process 
- View result as json string

![alt text](uc2-image2.png "Snapshot 2")
