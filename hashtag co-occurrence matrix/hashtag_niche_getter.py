import re
from itertools import combinations
from api_requests import get_hashtag_id, get_top_media,get_recent_media,add_post_id
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import shutil


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')
ACCESS_TOKEN = os.getenv('app1token')
USER_ID = os.getenv('user1_id')


niche_hashtags_fitness = '#fitness#fitnessmotivation#fitnessmodel#fitnessaddict#fitnessgirl#fitnessjourney#fitnesslifestyle#fitnesslife#fitnessfreak#fitnessgoals#fitnessgear#fitnessfood#fitnessinspiration#fitnessgirls#fitnessbody#fitnesswomen#fitnessblogger#fitnessmodels#fitnesscoach#fitnessphysique#fitnessmom#FitnessTrainer#fitnesslover#fitnessaddicted#fitnessfreaks#fitnesstips#fitnessboy#fitnessfirst#fitnessquote#fitnessgoal'.split('#')
niche_hashtags_etsy = '#etsy#etsyshop#etsyseller#etsyfinds#etsystore#etsylove#etsysellersofinstagram#etsygifts#etsyuk#etsyhandmade#etsysellers#etsysale#etsyshopowner#etsyusa#etsyhunter#etsyelite#etsyvintage#etsyfind#etsyau#etsybaby#etsyartist#etsysellerofinstagram#etsyfavorites#etsysuccess#etsyart#etsywedding#etsyfashion#etsymaker'.split("#")
niche_hashtags = list(map(lambda x: x.lower(), niche_hashtags_etsy))
niche_hashtags.remove("")
last_hashtag = "etsyfashion"
niche_hashtags = niche_hashtags[niche_hashtags.index(last_hashtag):]


l=["customsneakers","sneakersoriginal","buckethat","buckethats","wristwatchlovers","wristwatch","wristwatches","wristwatchcheck"]







def extract_hashtags(caption):
    if not caption:
        return []
    return re.findall(r"#\w+", caption.lower())



def update_co_occur_matrix(hashtags,co_occur,post_id):
    hashtags = list(set(hashtags))
    posts_df_path = os.path.join('hashtag co-occurrence matrix', 'posts_df.csv')
    posts_df = pd.read_csv(posts_df_path)
    if post_id not in posts_df['id'].values:
        
        for h1, h2 in combinations(hashtags, 2):
            
            
            pair = tuple(sorted([h1, h2]))
            mask = (co_occur["hashtag_a"] == pair[0]) & (co_occur["hashtag_b"] == pair[1])
            
            if mask.any():
                co_occur.loc[mask, "co_occur"] += 1
                # print(f"Updated value for {h1},{h2}:",co_occur.loc[mask, "co_occur"])
            else:
                co_occur.loc[len(co_occur)] = {"hashtag_a": pair[0], "hashtag_b": pair[1], "co_occur": 1}
                
                # print(f"Added new pair: {pair[0]} and {pair[1]}")

    else:
        print('post already checked, no need to update')



def sort_co_occur_matrix(co_occur):
    co_df_sorted = co_occur.sort_values(by="co_occur", ascending=False)
    return co_df_sorted



def read_hashtags(hashtags):
    df_path = os.path.join('hashtag co-occurrence matrix', 'co-occur.csv')
    temp_path = df_path + '.tmp'
    
    # Read the CSV in chunks to handle large files
    chunk_size = 10000  # Adjust this based on your available memory
    co_occur = pd.concat(pd.read_csv(df_path, chunksize=chunk_size))
    
    # Load existing post IDs once
    posts_df_path = os.path.join('hashtag co-occurrence matrix', 'posts_df.csv')
    existing_posts = pd.read_csv(posts_df_path)['id'].astype(str).values
    
    for hashtag in hashtags:
        print(f"\nProcessing hashtag: {hashtag}")
        hashtag_id = get_hashtag_id(hashtag, USER_ID, ACCESS_TOKEN)
        if not hashtag_id:
            print(f"Could not get ID for hashtag: {hashtag}")
            continue
            
        posts = get_top_media(hashtag_id, USER_ID, ACCESS_TOKEN)
        
        if len(posts)==0:
            print(f"Found {len(posts)} top media posts for {hashtag}, trying recent media")
            posts = get_recent_media(hashtag_id,USER_ID,ACCESS_TOKEN)
        for post in posts:
            post_id = str(post['id'])
            if post_id in existing_posts:
                print(f"Post {post_id} already processed, skipping...")
                continue
                
            add_post_id(post)
            caption = post.get('caption', '')
            if caption:
                hashtags_in_post = extract_hashtags(caption)
                if hashtags_in_post:
                    print(f"Found {len(hashtags_in_post)} hashtags in post {post_id}")
                    update_co_occur_matrix(hashtags_in_post, co_occur, post_id)
            else:
                print(f'No caption in post {post_id}')
            
            # Save the updated matrix periodically
            co_df_sorted = sort_co_occur_matrix(co_occur)
            co_df_sorted.to_csv(temp_path, index=False)
            shutil.move(temp_path, df_path)
            print("Updated co-occurrence matrix")

            
                
    
read_hashtags(l)







def change_to_int():


    # Paths
    df_path = os.path.join('hashtag co-occurrence matrix', 'co-occur.csv')
    temp_path = df_path + '.tmp'
    df_path2= os.path.join('hashtag co-occurrence matrix', 'co-occur2.csv')
    # Load and fix
    df = pd.read_csv(df_path)
    df['co_occur'] = df['co_occur'].fillna(0).astype(int)

    # Save safely
    df.to_csv(df_path2, index=False)
    shutil.move(temp_path, df_path2)

    
    





def compare_dfs(df1, df2):
    """
    Compare two DataFrames and return differences in rows and columns.
    Assumes same columns. If not, will highlight that too.

    Returns a dict with keys:
      - 'shape_mismatch'
      - 'column_diff'
      - 'rows_only_in_df1'
      - 'rows_only_in_df2'
      - 'different_values'
    """
    result = {}

    # Shape check
    if df1.shape != df2.shape:
        result['shape_mismatch'] = (df1.shape, df2.shape)

    # Column check
    if list(df1.columns) != list(df2.columns):
        result['column_diff'] = {
            'only_in_df1': list(set(df1.columns) - set(df2.columns)),
            'only_in_df2': list(set(df2.columns) - set(df1.columns))
        }

    # Row differences
    df1_only = pd.concat([df1, df2]).drop_duplicates(keep=False)
    df2_only = pd.concat([df2, df1]).drop_duplicates(keep=False)

    if not df1_only.empty:
        result['rows_only_in_df1'] = df1_only
    if not df2_only.empty:
        result['rows_only_in_df2'] = df2_only

    # If same shape and columns, check cell-by-cell differences
    if df1.shape == df2.shape and list(df1.columns) == list(df2.columns):
        diff_mask = (df1 != df2) & ~(df1.isna() & df2.isna())
        if diff_mask.any().any():
            differences = []
            for row, col in zip(*diff_mask.to_numpy().nonzero()):
                differences.append({
                    'row': row,
                    'column': df1.columns[col],
                    'df1': df1.iat[row, col],
                    'df2': df2.iat[row, col]
                })
            result['different_values'] = differences

    return result

    


def clean_cooccur_csv():
    df_path = os.path.join('hashtag co-occurrence matrix', 'co-occur.csv')
    """
    Loads a CSV file, removes rows where co_occur == 1,
    and saves the cleaned DataFrame back to the same file.

    Parameters:
        file_path (str): Path to the CSV file. Default is 'co-occur.csv'.
    """
    # Load the CSV file
    df = pd.read_csv(df_path)

    # Filter out rows with co_occur == 1
    df_cleaned = df[df['co_occur'] > 1]

    # Save the cleaned DataFrame back to the CSV
    df_cleaned.to_csv(df_path, index=False)

    print(f"Cleaned data saved to {df_path}")


