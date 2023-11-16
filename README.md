# What are the Odds?

This repo is my solution to the following [Developper Test](https://github.com/lioncowlionant/developer-test)


I decided to use Python to solve this test. Since I don't have great expertise in building frontend, I opted to build the web app using [Streamlit](https://streamlit.io/). 

## Setting you up

I recommend using a dedicated conda env:

```
conda create -n devtest python=3.8
conda activate devtest
pip install streamlit
```

## CLI

Running the `r2d2.sh` script will give you the odds of reaching the destination given your millenium and empire files:

```
cmod +x r2d2.sh
./r2d2.sh examples/example1/millennium-falcon.json examples/example1/empire.json
```

## Front end

To run the front end, use streamlit:

```
streamlit run c3po.py
```

## Examples

I added an example (example 5) to showcase an option where the vessel can go back to previous planets in order to have better odds of going to Endor. This is to sanity check my implementation of bidirectional edges (space jump can be done in both directions). 