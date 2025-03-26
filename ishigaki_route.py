import folium
import pandas as pd

# 读取数据
df = pd.read_csv('locations.csv')

# 创建底图（石垣岛中心坐标）
m = folium.Map(location=[24.3444, 124.1558], zoom_start=12, tiles='OpenStreetMap',
               control_scale=True)

# 美观的颜色方案
COLOR_SCHEME = {
    '景点': {
        'icon': 'star',  # Font Awesome 图标
        'color': '#3498db',  # 柔和的蓝色
        'shadow': '#2980b9',
    },
    '餐厅': {
        'icon': 'utensils',  # Font Awesome 图标（原 cutlery 已弃用，改用 utensils）
        'color': '#e74c3c',  # 柔和的红色
        'shadow': '#c0392b',
    }
}

# 添加标记
for index, row in df.iterrows():
    # 创建弹出窗口内容
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 300px;">
        <h3 style="color: {COLOR_SCHEME[row['类型']]['color']}; margin-bottom: 5px;">{row['名称']}</h3>
        <p style="color: #555; font-size: 14px; margin-top: 0;">{row['简介']}</p>
        <img src="{row['图片链接']}" style="width: 100%; border-radius: 5px;">
    </div>
    """
    iframe = folium.IFrame(html, width=350, height=250)
    popup = folium.Popup(iframe, max_width=350)

    # 获取当前类型的颜色配置
    colors = COLOR_SCHEME[row['类型']]

    # 创建带图标 + 文本的标记
    icon_html = f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 15pt;
        font-weight: bold;
        font-family: Arial, sans-serif;
        color: {colors['color']};
        text-shadow: 1px 1px 2px {colors['shadow']};
        padding: 2px 8px;
        border-radius: 12px;
        white-space: nowrap;
    ">
        <i class="fa fa-{colors['icon']}" style="font-size: 14px;"></i>
        {row['名称']}
    </div>
    """

    # 添加标记
    folium.Marker(
        location=[row['纬度'], row['经度']],
        popup=popup,
        icon=folium.DivIcon(
            icon_size=(150, 36),  # 调整大小以适应文本
            icon_anchor=(75, 18),
            html=icon_html
        )
    ).add_to(m)

# 确保加载 Font Awesome（用于图标）
m.get_root().html.add_child(folium.Element("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
"""))

# 保存地图
m.save('ishigaki_travel_map.html')