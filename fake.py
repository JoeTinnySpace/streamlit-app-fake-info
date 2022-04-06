import streamlit as st
from pandas import read_excel
from openpyxl import load_workbook

st.title("""Fake chart""")
# st ELEMENT
uploaded_file = st.file_uploader("""Upload fake raw data file: """)

flag = 0

# st ELEMENT
my_bar = st.progress(0)

if uploaded_file == None:
    st.write("""
    ### Load file using browse files!
    """)
else:
    # st ELEMENT
    my_bar.progress(1)
    st.write(""" ## Alleppey cluster Fake attempts""")

    my_bar.progress(10)
    possible_sheet_name = ["raw data", "fake tids"]
    wb = load_workbook(uploaded_file)
    my_bar.progress(25) 
    sheetname = [book for book in wb.sheetnames if (book.lower() in possible_sheet_name)]
    try:
        print('Generating dataframe...')
        df = read_excel(uploaded_file, sheet_name=sheetname[0])
        flag = 1
    except Exception as e:
        st.Error(e)
if (flag):
    #check if hubname is a column header or not
    if 'Hub Name' in df:
        hub_name = 'Hub Name'
    elif 'hub_name' in df:
        hub_name = 'hub_name'
    # elif '' in df:
        # hub_name = ''
    
    COLUMNS = [hub_name, 'fake_detection_reason', 'geo_distance' ,'vendor_tracking_id', 'undel_unpick_status',
                'agent_name', 'Kirana']
    HUBS = ['AlleppeyHub_ALP','CharumoodHub_COO','ChengannurHub_CNN', 'Cherthala_CTA',
            'KaruvattaHub_KVT', 'KayamkulamHub_KKM', 'SASThuravoorODH_THO', 'STCMuthukulamODH_MKL']
    EXCLUSION_LIST = ['DELIVERED', 'UNDELIVERED']
    # HUBS = ['AlleppeyHub_ALP']     
    my_bar.progress(50)
    print('Counting the distance...')
    # rounding the distance unit ( TODO : make it in KM)
    df.loc[:, "geo_distance"] = df["geo_distance"].map('{:.2f}'.format)
    my_bar.progress(65)
    print('Filtering dataframe and sorting...')
    # filtering dataframe based on hub_name with HUBS list, and sorting alphabetically.
    filtered_df = df.loc[df[hub_name].isin(HUBS), COLUMNS].sort_values(hub_name)
    my_bar.progress(75)
    print('More filtering... We dont need delivered fake...')
    # removing delivered fakes
    filtered_df = filtered_df.loc[~filtered_df['undel_unpick_status'].isin(EXCLUSION_LIST)]
    my_bar.progress(90)
    print('Styling the dataframe...')
    # styling for the dataframe
    styled_df = filtered_df.style.set_table_styles(
        [{'selector' : 'th',
            'props' : [('background', '#ea6154'),
                        ('color' , '#fff3ef'),
                        ('font-family', 'helvetica'),
                        ('text-align', 'left')]},
        {'selector' : 'td',
            'props' : [('text-align', 'left'),
                        ('font-family', 'helvetica')]
        },
        {'selector' : 'tr:nth-of-type(odd)',
            'props' : [('background', '#DCDCDC')]
        },
        {'selector' : 'tr:nth-of-type(even)',
            'props' : [('background', 'white')]
        }
        ]
    )
    # st ELEMENT
    my_bar.progress(100)
    st.table(styled_df)
    my_bar.empty()
