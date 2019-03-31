from IPython.display       import HTML, Markdown

def color(text, color = 'red', background = 'transparent', weight = 'normal') :
    return f'<span style="color:{color};background:{background};font-family:monospace;font-weight:{weight}">{text}</span>'

def html(*objects, sep = ' ', monospaced = False) :
    text = sep.join(str(o) for o in objects)
    text = f'<span style="font-family:monospace"><pre>{text}</pre></span>' if monospaced else \
           f'<span                              ><pre>{text}</pre></span>'
    return display(HTML(text))

def mark(*objects, sep = ' ', monospaced = False) :
    text = sep.join(str(o) for o in objects)
    text = f'<span style="font-family:monospace">{text}</span>' if monospaced else \
           f'<span                              >{text}</span>'
    return display(Markdown(text))

def hr(header = '', color = 'black') :
    return html(f'<fieldset style="border:0px;border-top:2px solid {color}"><legend><b>{header}</b></legend></fieldset>') if header else \
           html(f'<hr       style="border:0px;border-top:2px solid {color}"/>')

def sand() :
    return True

def comp(df, verbose = True) :

    pre = df.memory_usage().sum() / 1024**2 / 8
    
    integer = {np.iinfo(np.int8   ).max : np.int8,
               np.iinfo(np.int16  ).max : np.int16,
               np.iinfo(np.int32  ).max : np.int32,
               np.iinfo(np.int64  ).max : np.int64}
    inexact = {np.finfo(np.float16).max : np.float16,
               np.finfo(np.float32).max : np.float32,
               np.finfo(np.float64).max : np.float64}

    for col in df.columns :
        if  np.issubdtype(df[col].dtype, np.inexact) :
            df[col] = df[col].astype(inexact.get(min((n for n in inexact.keys() if n > max(df[col].max(), abs(df[col].min()))))))
        if  np.issubdtype(df[col].dtype, np.integer) :
            df[col] = df[col].astype(integer.get(min((n for n in integer.keys() if n > max(df[col].max(), abs(df[col].min()))))))

    end = df.memory_usage().sum() / 1024**2 / 8

    if  verbose :
        print(f'Memory Use Reduced to {end:5.2f} MB [{100 * (pre - end) / pre:.1f}% Reduction]')
    
    return df
    
def compress(df, verbose = True) :

    pre = df.memory_usage().sum() / 1024**2 / 8

    integer = ([np.int8,   np.int16,   np.int32,   np.int64], np.iinfo)
    inexact = ([         np.float16, np.float32, np.float64], np.finfo)

    for col in df.columns :
        types = integer if df[col].dtype in integer[0] else \
                inexact if df[col].dtype in inexact[0] else None
        if  types :
            amax = max(df[col].max(), abs(df[col].min()))
            cmin = df[col].min()
            cmax = df[col].max()

            for kind in types[0] :
                if  cmin > types[1](kind).min and \
                    cmax < types[1](kind).max     :
                    df[col] = df[col].astype(kind)
                    break
                    
          # print(col, df[col].dtype, amax)

    end = df.memory_usage().sum() / 1024**2 / 8

    if  verbose :
        print(f'Memory Use Reduced to {end:5.2f} MB [{100 * (pre - end) / pre:.1f}% Reduction]')
    
    return df

def numerize(dfs) :

    frame    = defaultdict(list)
    types    = defaultdict(list)
    encoders = defaultdict(None)
    
    for df in dfs :
        for col in df :
            frame[col].append(df)
            types[col].append(df[col].dtype)

    for col in types :
        
        print(f'column {col:<27} is present in {len(frame[col])} dataframes. {types[col]}')
        
        
        
        encoders[col] = LabelEncoder()
        
    hr()
    for df in dfs :
        for col in df :
            if  df[col].dtype == object :
                print(col)
            
    return df

  # numerize([transactions_old,transactions_new,merchants,train,test])
