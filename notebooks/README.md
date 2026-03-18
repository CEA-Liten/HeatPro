# Conversion Notebook

To ensure that `plotly` graphs are displayed correctly during conversion, the notebook must contain the following command:

```python
import plotly.io as pio
pio.renderers.default='notebook'
```

To convert the notebook to HTML, enter the following command in a terminal:

```
uv run --group notebook jupyter nbconvert [path to notebook] --to html --no-input --embed-images --output-dir [path to notebook]/_html_build
```

`--to html` specifies that the output format is HTML.

`--no-input` indicates that the code should not be displayed.

`--embed-images` specifies that images should be embedded in base 64 within the HTML.

`--output-dir [path to notebook]/_html_build` specifies the export folder.

To format the HTML as A4 size, override the `body` with the following script:

```html
html {
   background-color: #D8D8D8;
}

body {
 color: #FFFFFF;
 max-width: 21cm;
 margin-left: auto;
 margin-right: auto;
 color: var(--jp-ui-font-color1);
 font-size: var(--jp-ui-font-size1);
}
```
