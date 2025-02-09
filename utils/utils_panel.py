import plotly.express as px


# Funcion para crear columna de tipo de cartonere
def determinar_tipo_cartonero(row):
    if row['legacyId'].startswith('LE'):
        val = 'LE'
    elif row['legacyId'] == 'No especificado':
        val = 'No especificado'
    else:
        val = 'RA'
    return val


def crear_df_filtrado(df, predios, fecha_inicio, fecha_finalizacion, materiales, tipo_cartonero):
    df_filtrado = df.copy()

    # Crear columna de tipos de cartoneres
    df_filtrado['tipoCartonero'] = df_filtrado.apply(determinar_tipo_cartonero, axis=1)

    # Aplicar filtros
    df_filtrado = df_filtrado.loc[df_filtrado['predio'].isin(predios)]
    df_filtrado = df_filtrado[(df_filtrado['fecha'] >= fecha_inicio) & (df_filtrado['fecha'] <= fecha_finalizacion)]
    df_filtrado = df_filtrado.loc[df_filtrado['material'].isin(materiales)]
    df_filtrado = df_filtrado.loc[df_filtrado['tipoCartonero'].isin(tipo_cartonero)]

    return df_filtrado


def pesos_historico(data, operacion='promedio'):
    if operacion == 'promedio':
        df = data.groupby(by=['fecha', 'predio'], ).mean()
    else:
        df = data.groupby(by=['fecha', 'predio'], ).sum()
    df.reset_index(inplace=True)
    fig = px.scatter(df, x="fecha", y="peso", color="predio", size="peso")
    return fig

def pesos_historico_predios(data):
    '''
    Grafica fecha contra peso (promedio o suma total) entregado ese día agrupando según el predio.
    Devuelve la figura de plotly conteniendo el gráfico.
    '''
    df = data.groupby(by=["fecha", "predio", "material"], as_index = False).sum()    # Para sacar la info de materiales, sacar "material"
    fig = px.bar(df, x="fecha", y="peso", color="predio", barmode = "group", hover_data=["material"])
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])    # Ignora fin de semana

    fig.update_traces(
        hovertemplate ='<br><b>Peso</b>: %{y} Kg<br>',
    ),
    fig.update_layout(
        showlegend=False,
        hovermode="x unified",
        xaxis_tickformat = '%d-%m-%Y',
        yaxis_tickformat = 'digit',
        paper_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white"),

        xaxis=dict(
            zeroline=False,
            showgrid=False,
            showticklabels=True,
            mirror=True,
            ticks="outside",
            tickfont=dict(family="Arial",
                          size=13,
                          color="rgb(0,0,0)",),
            ),

        yaxis=dict(
            showgrid=True,
            zeroline=False,
            mirror=True,
            ticks="outside",
            tickfont=dict(family="Arial",
                          size=13,
                          color="rgb(0,0,0)")),
        xaxis_title=dict(text="Fecha",
                         font=dict(
                             size=15,
                             color="rgb(0,0,0)",)
                        ),
        yaxis_title=dict(text="Kilos (Kg)",
                         font=dict(
                                   size=15,
                                   color="rgb(0,0,0)",)),
        )



    return fig


def torta(data):
    df = data.groupby(by=['material'], ).sum()
    df.reset_index(inplace=True)
    fig = px.pie(df, values='peso', names='material', title='')
    fig.update_traces(hoverinfo="label+percent", textfont_size=14,
                      textinfo="percent", marker=dict(line=dict(color="#FFFFFF", width=0.1)),
                      textposition="auto")

    fig.update_traces(
        hovertemplate ='<b>%{label}<b><br><br><b>Peso</b>: %{value} Kg<br>')

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        legend = dict(orientation = "h",   # show entries horizontally
                     xanchor = "center",  # use center of legend as anchor
                     x = 0.5)

        )

    return fig
