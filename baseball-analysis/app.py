import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- ページ設定 ---
st.set_page_config(
    page_title="野球データ分析アプリ",
    page_icon="⚾",
    layout="wide"
)

# --- タイトル ---
st.title("⚾ プロ野球データ分析アプリケーション")
st.markdown("NPBの年度別成績データを分析・可視化します。")

# --- データ読み込み ---
@st.cache_data
def load_data(file_type):
    filepath = f'data/{file_type}.csv'
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except (UnicodeDecodeError, FileNotFoundError):
        try:
            df = pd.read_csv(filepath, encoding='cp932')
        except Exception as e:
            st.error(f"エラー: ファイル '{filepath}' の読み込みに失敗しました。詳細: {e}")
            return pd.DataFrame()
    return df

batting_df = load_data("batting")
pitching_df = load_data("pitching")

# --- サイドバー ---
st.sidebar.header("分析条件の設定")
analysis_target = st.sidebar.radio("分析対象を選択してください:", ("打撃成績", "投手成績"))

# --- データ加工と指標の選択 ---
if analysis_target == "打撃成績":
    df = batting_df.copy()
    if '打数' in df.columns and '打率' in df.columns and '長打' in df.columns:
        df['長打率'] = df['長打'] / df['打数']
        df['ISO'] = df['長打率'] - df['打率']
    if '四球' in df.columns and '三振' in df.columns:
        df['BB/K'] = df['四球'] / df['三振'].replace(0, np.nan)
    
    main_metrics = ['打率', '本塁打', '打点', 'OPS', '盗塁', 'ISO', 'BB/K']
    sort_key_default = 'OPS'
    min_at_bats = st.sidebar.slider("規定打席数の下限", 0, 600, 0)
    if '打数' in df.columns:
        df = df[df['打数'] >= min_at_bats]
else:
    df = pitching_df.copy()
    if '奪三振' in df.columns and '与四球' in df.columns:
        df['K/BB'] = df['奪三振'] / df['与四球'].replace(0, np.nan)
        
    main_metrics = ['防御率', '勝利', '敗戦', 'セーブ', '奪三振', 'WHIP', '投球回', 'K/BB']
    sort_key_default = '防御率'
    min_innings = st.sidebar.slider("規定投球回の下限", 0, 200, 0)
    if '投球回' in df.columns:
        df = df[df['投球回'] >= min_innings]

main_metrics = [m for m in main_metrics if m in df.columns and df[m].notna().any()]
years = sorted(df['年度'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("年度を選択してください:", years)
teams = ['全チーム'] + sorted(df['チーム'].unique().tolist())
selected_team = st.sidebar.selectbox("チームを選択してください:", teams)

team_colors = {
    '巨人': 'orange', '広島': 'red', 'DeNA': 'blue', '中日': 'skyblue',
    '阪神': 'gold', 'ヤクルト': 'green'
}

# --- メインコンテンツ ---
filtered_df = df[df['年度'] == selected_year].copy()
if selected_team != '全チーム':
    filtered_df = filtered_df[filtered_df['チーム'] == selected_team]

st.header(f"📊 {selected_year}年 {selected_team} {analysis_target}")
st.dataframe(filtered_df.style.format({
    '打率': '{:.3f}', 'OPS': '{:.3f}', '防御率': '{:.2f}', 'WHIP': '{:.2f}',
    'ISO': '{:.3f}', 'BB/K': '{:.2f}', 'K/BB': '{:.2f}', '長打率': '{:.3f}'
}))

csv_string = filtered_df.to_csv(index=False, encoding='utf-8-sig')
st.download_button("このデータをCSVでダウンロード", csv_string, f'{selected_year}_{selected_team}_{analysis_target}.csv', 'text/csv')
st.markdown("---")

# --- 指標別ランキングと可視化 ---
st.header("🏆 指標別ランキング")
col1, col2 = st.columns([1, 2])
with col1:
    rank_metrics = [m for m in main_metrics if m in filtered_df.columns]
    try:
        default_index = rank_metrics.index(sort_key_default)
    except ValueError:
        default_index = 0
    sort_key = st.selectbox("ランキングの基準となる指標:", rank_metrics, index=default_index)
    top_n = st.slider("表示する上位選手の人数:", min_value=3, max_value=30, value=10)

if not filtered_df.empty and sort_key:
    is_ascending = sort_key in ['防御率', 'WHIP', '敗戦']
    ranking_df = filtered_df.dropna(subset=[sort_key]).sort_values(by=sort_key, ascending=is_ascending).head(top_n)

    with col2:
        # ★★★ 修正点① ★★★
        fig = px.bar(
            ranking_df, x='選手名', y=sort_key, color='チーム', color_discrete_map=team_colors,
            title=f'{selected_year}年 {sort_key} トップ{top_n}',
            labels={'選手名': '選手', sort_key: sort_key},
            text_auto='.3f' # 'text_auto'をここに追加
        )
        # fig.update_traces(...) の行を削除
        fig.update_layout(xaxis_title="", yaxis_title=sort_key)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("表示するデータがありません。")

st.markdown("---")

# --- 散布図による相関分析機能 ---
st.header("2指標の相関分析 (散布図)")
scatter_df = df[df['年度'] == selected_year]
if not scatter_df.empty:
    scatter_metrics = [m for m in main_metrics if m in scatter_df.columns]
    col1_scatter, col2_scatter = st.columns(2)
    with col1_scatter:
        x_axis = st.selectbox("X軸の指標を選択", scatter_metrics, index=0, key="x_axis")
    with col2_scatter:
        y_axis = st.selectbox("Y軸の指標を選択", scatter_metrics, index=1, key="y_axis")

    if x_axis and y_axis:
        fig_scatter = px.scatter(
            scatter_df.dropna(subset=[x_axis, y_axis]), x=x_axis, y=y_axis,
            color="チーム", color_discrete_map=team_colors,
            hover_name="選手名", hover_data=['チーム'],
            title=f"{selected_year}年: {x_axis} vs {y_axis}"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("散布図を表示するデータがありません。")

st.markdown("---")

# --- チーム別成績比較 ---
st.header(f"⚔️ {selected_year}年 チーム別成績比較")
team_data_for_year = df[df['年度'] == selected_year]
if not team_data_for_year.empty:
    agg_metrics = [m for m in main_metrics if m in team_data_for_year.columns and pd.api.types.is_numeric_dtype(team_data_for_year[m])]
    team_agg_df = team_data_for_year.groupby('チーム')[agg_metrics].mean().reset_index()
    
    team_plot_metric = st.selectbox("比較する指標を選択:", agg_metrics, key="team_metric")
    is_team_ascending = team_plot_metric in ['防御率', 'WHIP', '敗戦']
    team_agg_df = team_agg_df.sort_values(by=team_plot_metric, ascending=is_team_ascending)

    # ★★★ 修正点② ★★★
    fig_team = px.bar(
        team_agg_df, x='チーム', y=team_plot_metric, color='チーム', color_discrete_map=team_colors,
        title=f'{selected_year}年 チーム別 {team_plot_metric} 比較',
        labels={'チーム': 'チーム', team_plot_metric: team_plot_metric},
        text_auto='.3f' # 'text_auto'をここに追加
    )
    # fig_team.update_traces(...) の行を削除
    st.plotly_chart(fig_team, use_container_width=True)
else:
    st.warning("比較するデータがありません。")

st.markdown("---")

# --- 選手個人の成績推移 ---
st.header("選手個人の年度別成績推移")
all_players_df = df if selected_team == '全チーム' else df[df['チーム'] == selected_team]
players = sorted(all_players_df['選手名'].unique())
if players:
    selected_player = st.selectbox("選手を選択してください:", players, key="player_select")
    player_df = df[df['選手名'] == selected_player]
    if not player_df.empty:
        st.subheader(f"{selected_player}選手の成績推移")
        plot_metrics = [m for m in main_metrics if m in player_df.columns and player_df[m].notna().any()]
        plot_metric = st.selectbox("グラフで表示する指標を選択してください:", plot_metrics, key="plot_metric")
        if plot_metric:
            fig_player = px.line(
                player_df, x='年度', y=plot_metric,
                title=f'{selected_player}選手の{plot_metric}推移',
                markers=True, text=plot_metric
            )
            fig_player.update_traces(textposition="top center")
            fig_player.update_layout(xaxis_title="年度", yaxis_title=plot_metric)
            st.plotly_chart(fig_player, use_container_width=True)
else:
    st.warning("表示する選手がいません。")

# --- 指標の解説セクション ---
with st.expander("主要な野球指標の解説を見る"):
    st.markdown("""
    | 指標 | 説明 | 計算式 |
    | :--- | :--- | :--- |
    | **打率 (AVG)** | 打者がヒットを打つ確率を示す指標。 | `安打数 / 打数` |
    | **OPS** | 出塁能力と長打力を足し合わせた、総合的な攻撃力を示す指標。 | `出塁率 + 長打率` |
    | **ISO** | 長打力を測る指標。数値が高いほどパワーヒッター。 | `長打率 - 打率` |
    | **BB/K** | 四球と三振の比率。1.0を超えると優秀な選球眼を持つとされる。 | `四球 / 三振` |
    | **防御率 (ERA)** | 投手が9イニングを投げた場合に平均何点取られるかを示す指標。 | `(自責点 * 9) / 投球回` |
    | **WHIP** | 1イニングあたりに何人の走者（ヒットと四球）を出したかを示す指標。 | `(与四球 + 被安打) / 投球回` |
    | **K/BB** | 奪三振と与四球の比率。3.5を超えると優秀とされる。 | `奪三振 / 与四球` |
    """)
