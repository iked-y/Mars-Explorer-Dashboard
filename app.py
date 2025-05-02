import dash
from dash import html, dcc, Output, Input
import plotly.graph_objs as go
import requests
import datetime
from PIL import Image
from io import BytesIO
import base64
import math

# API設定
API_KEY = '6e4wOzDfftp5e7ceKj9mUrxz9X6ckbkiQEnhXeLF'
ROVER_NAME = 'curiosity'

# アプリ初期化
app = dash.Dash(__name__)
# app.title = "Mars Explorer Dashboard"
app.title = "Mars Weather Dashboard"
# app.title = "What's the weather on Mars?"

# 固定画像のbase64変換
def encode_image(image_path):
    with open(image_path, 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()

earth_img_tmp = encode_image("./data/earth_spring_temperature_with_topo.png")
earth_img_p = encode_image("./data/earth_spring_mslp_with_topo.png")
earth_img_topo = encode_image("./data/earth_topography_map.jpg")
mars_img_tmp = encode_image("./data/mars_spring_temperature_with_geoh.png")
mars_img_p = encode_image("./data/mars_spring_surface-pressure_areoid-corrected_with_geoh.png")
mars_img_topo = encode_image("./data/mars_topography_map.jpg")

app.layout = html.Div([
    html.H1("🌦️ Mars Weather Dashboard", style={
        "textAlign": "center", 
        "padding": "20px", 
        "fontFamily": "Arial, sans-serif", 
        "color": "#333"
    }),

    dcc.Tabs([
        dcc.Tab(label='🚀 About Mars', children=[
            html.Div([
                html.H3("火星とは？", style={
                        "textAlign": "top", 
                        "marginBottom": "10px", 
                        "fontSize": "24px", 
                        "fontWeight": "bold"
                }),
                html.Div([
                    html.Span("火星は地球の約半分の大きさで、重力は約3分の1です。", style={
                        "display": "block",
                        "fontWeight": "regular"
                    }),
                    html.Span("大気は非常に薄く、主に二酸化炭素で構成されています。雨や雪は降らず、水は主に極地や地下に氷の状態で存在します。", style={
                        "display": "block",
                        "fontWeight": "regular"
                    }),
                    html.Span("表面には巨大な火山(~10km)や深い渓谷が広がり、地形は地球とは大きく異なります。また、数火星年に一度、惑星全体を覆う大規模な砂嵐も発生します。", style={
                        "display": "block",
                        "fontWeight": "regular"
                    })
                ], style={
                    "textAlign": "top", 
                    "marginBottom": "10px", 
                    "fontSize": "17px", 
                }),

                html.Div([
                    html.Div([
                        html.H4("Earth topography map", style={
                            "textAlign": "center", 
                            "marginBottom": "10px", 
                            "fontSize": "18px", 
                            "fontWeight": "bold"
                        }),
                        html.Img(src=earth_img_topo, style={
                            'width': '95%', 
                            'maxHeight': '40vh', 
                            'objectFit': 'contain', 
                            'border': '1px solid #ccc', 
                            'padding': '10px', 
                            'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'
                        })
                    ], style={"flex": "1", "marginRight": "10px"}),

                    html.Div([
                        html.H4("Mars topography map", style={
                            "textAlign": "center", 
                            "marginBottom": "10px", 
                            "fontSize": "18px", 
                            "fontWeight": "bold"
                        }),
                        html.Img(src=mars_img_topo, style={
                            'width': '95%', 
                            'maxHeight': '40vh', 
                            'objectFit': 'contain', 
                            'border': '1px solid #ccc', 
                            'padding': '10px', 
                            'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'
                        })
                    ], style={"flex": "1"})
                ], style={
                    "display": "flex", 
                    "justifyContent": "space-between", 
                    "alignItems": "center"
                })
            ], style={
                'padding': '20px', 
                'backgroundColor': '#f9f9f9', 
                'borderRadius': '10px'
            })
        ]),
        
        dcc.Tab(label='📸 Curiosity/NAVCAM Images', children=[
            html.Div([
            html.H3("火星の地表画像", style={
                    "textAlign": "top", 
                    "marginBottom": "10px", 
                    "fontSize": "24px", 
                    "fontWeight": "bold"
            }),
                html.Div([
                    html.Span("NASAの火星探査機「Curiosity」が撮影した地表の画像です。", style={
                        "display": "block",
                        "fontWeight": "regular"
                    }),
                    html.Span("搭載されているNAVCAM（Navigation Camera）は、主に自律走行のために使われるモノクロカメラで、地形や岩石、地表の様子を詳細に捉えています。", style={
                        "display": "block",
                        "fontWeight": "regular"
                    }),
                ], style={
                    "textAlign": "top", 
                    "marginBottom": "10px", 
                    "fontSize": "17px", 
                }),

                html.Div([
                    html.Label(
                        "📅 Select Observation Date", 
                        style={
                            "fontWeight": "bold", 
                            "marginRight": "10px",
                            "fontSize": "20px"
                        }
                    ),
                    dcc.DatePickerSingle(
                        id='date-picker',
                        date=datetime.date.today(),
                        style={"marginBottom": "10px"}
                    )
                ], style={
                    "display": "flex", 
                    "alignItems": "center", 
                    "marginBottom": "20px"
                }),
                html.Div([
                    html.Img(id='mars-image-1', style={
                        'width': '30%', 
                        'maxHeight': '40vh', 
                        'objectFit': 'contain', 
                        'marginRight': '10px',
                        'border': '1px solid #ccc', 
                        'padding': '10px', 
                        'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'
                    }),
                    html.Img(id='mars-image-2', style={
                        'width': '30%', 
                        'maxHeight': '40vh', 
                        'objectFit': 'contain', 
                        'marginRight': '10px',
                        'border': '1px solid #ccc', 
                        'padding': '10px', 
                        'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'
                    }),
                    html.Img(id='mars-image-3', style={
                        'width': '30%', 
                        'maxHeight': '40vh', 
                        'objectFit': 'contain', 
                        'border': '1px solid #ccc', 
                        'padding': '10px', 
                        'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'
                    })
                ], style={
                    "display": "flex", 
                    "justifyContent": "center", 
                    'textAlign': 'center',
                    "alignItems": "center"
                })
            ], style={
                'padding': '20px',  
                'backgroundColor': '#f9f9f9',
                'borderRadius': '10px'
            })
        ]),

        dcc.Tab(label='🔬 InSight Weather Data', children=[
            html.Div([
                html.H3("🌤️ 最近の火星の天気", style={
                        "textAlign": "top", 
                        "marginBottom": "10px", 
                        "fontSize": "24px", 
                        "fontWeight": "bold"
                }),
                html.H3("NASAの火星探査機「InSight」が観測した気象データです。InSightは2018年11月に赤道付近のエリジウム平原に着陸し、気温・気圧・風速などを毎日観測しています。", style={
                        "textAlign": "top", 
                        "marginBottom": "10px", 
                        "fontSize": "17px", 
                        "fontWeight": "regular"
                }),

                # 横並びに2つのグラフを配置
                html.Div([
                    dcc.Graph(id='temp-pressure-graph', style={
                        "flex": "1", 
                        "marginRight": "10px"
                    }),
                    dcc.Graph(id='wind-graph', style={"flex": "1"})
                ], style={
                    "display": "flex", 
                    "justifyContent": "space-between", 
                    "alignItems": "center"
                })
            ], style={
                'padding': '20px', 
                'backgroundColor': '#f9f9f9', 
                'borderRadius': '10px'
            })
        ]),

        dcc.Tab(label='🌍 Global Temperature Maps', children=[
            html.Div([
                html.H3("🌡 火星の気温", style={
                        "textAlign": "top", 
                        "marginBottom": "10px", 
                        "fontSize": "24px", 
                        "fontWeight": "bold"
                }),
                html.H3("地球に比べてとても寒いです。大気が非常に薄いため日中と夜の寒暖差が激しく、日中は0℃近くまで上昇することもありますが、夜間は−100℃以下まで冷え込みます。", style={
                        "textAlign": "top", 
                        "marginBottom": "10px", 
                        "fontSize": "17px", 
                        "fontWeight": "regular"
                }),
                # 横並びに全球分布を配置
                html.Div([
                    html.Div([
                        html.H4("Earth", style={
                            "textAlign": "center", 
                            "marginBottom": "10px", 
                            "fontSize": "18px", 
                            "fontWeight": "bold"
                        }),
                        html.Img(src=earth_img_tmp, style={
                            'width': '95%', 
                            'maxHeight': '40vh', 
                            'objectFit': 'contain', 
                            'border': '1px solid #ccc', 
                            'padding': '10px', 
                            'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'
                        })
                    ], style={"flex": "1", "marginRight": "10px"}),

                    html.Div([
                        html.H4("Mars", style={
                            "textAlign": "center", 
                            "marginBottom": "10px", 
                            "fontSize": "18px", 
                            "fontWeight": "bold"
                        }),
                        html.Img(src=mars_img_tmp, style={
                            'width': '95%', 
                            'maxHeight': '40vh', 
                            'objectFit': 'contain', 
                            'border': '1px solid #ccc', 
                            'padding': '10px', 
                            'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'
                        })
                    ], style={"flex": "1"})
                ], style={
                    "display": "flex", 
                    "justifyContent": "space-between", 
                    "alignItems": "center"
                })
            ], style={
                'padding': '20px', 
                'backgroundColor': '#f9f9f9', 
                'borderRadius': '10px'
            })
        ]),

        dcc.Tab(label='🌍 Global Pressure Maps', children=[
            html.Div([
                html.H3("🌀 火星の気圧", style={
                        "textAlign": "top", 
                        "marginBottom": "10px", 
                        "fontSize": "24px", 
                        "fontWeight": "bold"
                }),
                html.H3("火星の気圧は平均約600Paと、地球の約1%しかありません。大気の密度が非常に低いため、秒速数十メートルの風が吹いても、体に感じる圧力は弱いとされています。ただし、この風はダストを舞い上げる力があり、局地的な砂嵐の原因にもなります。", style={
                        "textAlign": "top", 
                        "marginBottom": "10px", 
                        "fontSize": "17px", 
                        "fontWeight": "regular"
                }),
                # 横並びに全球分布を配置
                html.Div([
                    html.Div([
                        html.H4("Earth", style={
                            "textAlign": "center", 
                            "marginBottom": "10px", 
                            "fontSize": "18px", 
                            "fontWeight": "bold"
                        }),
                        html.Img(src=earth_img_p, style={
                            'width': '95%', 
                            'maxHeight': '40vh', 
                            'objectFit': 'contain', 
                            'border': '1px solid #ccc', 
                            'padding': '10px', 
                            'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'
                        })
                    ], style={"flex": "1", "marginRight": "10px"}),

                    html.Div([
                        html.H4("Mars", style={
                            "textAlign": "center", 
                            "marginBottom": "10px", 
                            "fontSize": "18px", 
                            "fontWeight": "bold"
                        }),
                        html.Img(src=mars_img_p, style={
                            'width': '95%', 
                            'maxHeight': '40vh', 
                            'objectFit': 'contain', 
                            'border': '1px solid #ccc', 
                            'padding': '10px', 
                            'boxShadow': '0px 4px 8px rgba(0,0,0,0.2)'
                        })
                    ], style={"flex": "1"})
                ], style={
                    "display": "flex", 
                    "justifyContent": "space-between", 
                    "alignItems": "center"
                })
            ], style={
                'padding': '20px', 
                'backgroundColor': '#f9f9f9', 
                'borderRadius': '10px'
            })
        ])

    ], style={
        "boxShadow": "0px 4px 12px rgba(0,0,0,0.1)", 
        "borderRadius": "10px", 
        "overflow": "hidden"
    })
], style={
    'height': '100vh', 
    'overflow': 'auto', 
    'fontFamily': 'Arial, sans-serif', 
    'backgroundColor': '#f0f0f0'
})

# コールバック：画像とグラフの更新
@app.callback(
    [Output('mars-image-1', 'src'),
     Output('mars-image-2', 'src'),
     Output('mars-image-3', 'src'),
     Output('temp-pressure-graph', 'figure'),
     Output('wind-graph', 'figure')],
    Input('date-picker', 'date')
)
def update_dashboard(selected_date):
    # --- NAVCAM画像取得 ---
    date_str = selected_date
    photo_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ROVER_NAME}/photos"
    params = {'earth_date': date_str, 'api_key': API_KEY}
    response = requests.get(photo_url, params=params)
    data = response.json()

    # デバッグ用: APIレスポンスを出力
    print("API Response:", data)

    photos = [p for p in data.get('photos', []) if p['camera']['name'] == 'NAV_LEFT_B']

    images = []
    num_photos = len(photos)

    # インデックスを均等に3つ選ぶ
    indices = []
    if num_photos <= 3:
        indices = list(range(num_photos))
    else:
        indices = [0, num_photos // 2, num_photos - 1]

    for i in indices:
        try:
            img_url = f"{photos[i]['img_src']}?cache_buster={datetime.datetime.now().timestamp()}"
            img_data = requests.get(img_url, timeout=5).content
            img = Image.open(BytesIO(img_data)).convert('L')
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            encoded_image = 'data:image/jpeg;base64,' + base64.b64encode(buffer.getvalue()).decode()
            images.append(encoded_image)
        except Exception as e:
            print(f"Error processing image at index {i}: {e}")
            images.append('')

    # デバッグ用: 画像の数を出力
    print("Number of images:", len(images))
    
    # --- InSight Weather データ取得 ---
    insight_url = f"https://api.nasa.gov/insight_weather/?api_key={API_KEY}&feedtype=json&ver=1.0"
    insight_data = requests.get(insight_url).json()
    sol_keys = sorted(insight_data.get('sol_keys', []), key=int)

    sols, temps, pressures, u_winds, v_winds, Spd, Dir = [], [], [], [], [], [], []

    for sol in sol_keys:
        d = insight_data.get(sol, {})
        at = d.get('AT', {})
        pre = d.get('PRE', {})
        wd = d.get('WD', {})
        if at.get('av') is not None and pre.get('av') is not None:
            sols.append(int(sol))
            temps.append(at['av'])
            pressures.append(pre['av'])
        if wd.get('most_common') and d.get('HWS'):
            deg = wd['most_common'].get('compass_degrees')
            speed = d['HWS'].get('av')
            if deg is not None and speed is not None:
                rad = math.radians(deg)
                u = speed * math.cos(rad)
                v = speed * math.sin(rad)
                u_winds.append(u)
                v_winds.append(v)
                Dir.append(deg)
                Spd.append(speed)

    # --- グラフ1：気温と気圧 ---
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=sols[:len(temps)], y=temps, name="Temperature (°C)", mode='lines+markers', line=dict(color='red')))
    fig1.add_trace(go.Scatter(x=sols[:len(temps)], y=pressures, name="Pressure (Pa)", mode='lines+markers', yaxis='y2', line=dict(color='blue', dash='dash')))
    fig1.update_layout(
        title="Temperature & Pressure (InSight)",
        xaxis_title="Sol",
        yaxis=dict(title='Temperature (°C)', color='red'),
        yaxis2=dict(title='Pressure (Pa)', overlaying='y', side='right', color='blue'),
        template='plotly_white',
        height=400,
        legend=dict(
        x=1,  # 凡例のx座標（右端: 1.0）
        y=1.3,  # 凡例のy座標（上端: 1.0）
        xanchor='right',  # 凡例の横方向のアンカー位置
        yanchor='top'     # 凡例の縦方向のアンカー位置
        )
    )

    # --- グラフ2：speed, direction ---
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=sols[:len(Spd)], y=Spd, name="Speed (m/s)", mode='lines+markers', line=dict(color='green')))
    fig2.add_trace(go.Scatter(x=sols[:len(Spd)], y=Dir, name="Direction (°)", mode='lines+markers', yaxis='y2', line=dict(color='gray', dash='dash')))
    fig2.update_layout(
        title="Winds (InSight)",
        xaxis_title="Sol",
        yaxis=dict(title='Wind speed (m/s)', color='green'),
        yaxis2=dict(title='Wind direction (°)', overlaying='y', side='right', color='gray'),
        template='plotly_white',
        height=400,
        legend=dict(
        x=1,  # 凡例のx座標（右端: 1.0）
        y=1.3,  # 凡例のy座標（上端: 1.0）
        xanchor='right',  # 凡例の横方向のアンカー位置
        yanchor='top'     # 凡例の縦方向のアンカー位置
        )
    )

    # # --- グラフ3：風速のU/V成分 ---
    # fig2 = go.Figure()
    # fig2.add_trace(go.Scatter(x=sols[:len(u_winds)], y=u_winds, name="U Component", mode='lines+markers', line=dict(color='green')))
    # fig2.add_trace(go.Scatter(x=sols[:len(v_winds)], y=v_winds, name="V Component", mode='lines+markers', line=dict(color='gray')))
    # fig2.update_layout(
    #     title="Wind Components (InSight)",
    #     xaxis_title="Sol",
    #     yaxis_title="Wind Speed (m/s)",
    #     template='plotly_white',
    #     height=400
    # )


    # 画像数に応じて分岐
    if len(images) == 0:
        return '', '', '', fig1, fig2  # 画像がない場合
    elif len(images) == 1:
        return images[0], '', '', fig1, fig2  # 画像が1つの場合
    elif len(images) == 2:
        return images[0], images[1], '', fig1, fig2  # 画像が2つの場合
    else:
        return images[0], images[1], images[2], fig1, fig2  # 画像が3つの場合


if __name__ == '__main__':
    app.run(debug=True)