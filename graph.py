import plotly.graph_objects as go
import pandas as pd
import base64


def to_img(json_data):
    json_df = pd.json_normalize(json_data)

    fig = go.Figure(data=[
        go.Bar(name='volume at Bid', y=json_df.price, x=json_df.volumeAtBid, orientation='h', text=json_df.volumeAtBid),
        go.Bar(name='volume at Ask', y=json_df.price, x=json_df.volumeAtAsk, orientation='h', text=json_df.volumeAtAsk)
    ], )

    fig.update_layout(barmode='stack', showlegend=False, xaxis_title="volume", yaxis_title="price", title="即時分價量")

    img_bytes = fig.to_image(format="png", width=600, height=350, scale=2)
    encoded = base64.b64encode(img_bytes)
    img_html = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))

    return img_html
