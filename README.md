# Failures in my Presentation to fix

* tell about yourself in begin of the presentation
* tell about the dataset
* use price / sqft
    this will remove influence of the sqft on the price and will let to compare more wisely
* explain, what is gonna to be proven in a presentation
    in beginning and in the end
* if I'm showning teh graph, especially teh complex one, I shoudl lead the audience attention
* make a font readable from notebook screen. bigger'
* track a prices weighted by month. mean over month - this will remove single spikes. exact 
    dates tracking was not important for the customer
* if customer is buyer, to select some houses, it is bnetter to start with a wide scope and 
    squeese it stepwise
* make a conclusion at the end
* make a recommendations at the end
* tell, how the result can be improved with the future investigations


plotly - this library can export the images in svg format with the transparent background

## export SVG geomaps with plotly

it uses kaleido and can't use relative path for geodata

```python
import os

rel_path = 'data/geodata.json'

abs_path = os.path.abspath(rel_path)
px.chloropleth_map([...], geojson=rel_path).show()
px.chloroplath_map([...], geojson=abs_path).write_image('./img/name.svg')
```

or

```python
px.write_image(
    fig,
    './img/name.svg',
    format = 'svg',
    width = 1600,
    height = '900')
```

```python
with open('./data/geo.json') as f:
    geojson_data = json.load(f)

```
