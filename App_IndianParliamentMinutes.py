import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast
from wordcloud import WordCloud

# Configure Streamlit settings
st.set_page_config(layout="centered", page_title="Indian Parliament Debates since 1952", page_icon="")

# Load the CSV file
df = pd.read_csv(r'C:\Users\vishe\Desktop\Indian Parliament\10final_abridged3.csv')


# Set larger font size for main title
st.markdown("<h1 style='font-family:Raleway; font-size: 2.8rem;'>Indian Parliament Debate since 1952</h1>", unsafe_allow_html=True)

# Set smaller font size for the note with italicized text
st.markdown("<p style='font-family:Roboto; font-size: 1.1rem; margin-top: 0.5rem;'><i>(I had known that the Lok Sabha website publishes the minutes of the parliamentary debates, but found the idea of rummaging through the 5,000 documents difficult. Here is my small attempt to take this massive truckload of information and make it more accessible. I hope it sparks your curiosity and encourages further exploration of this rich resource. Let me know if you have any suggestions to improve on visheshika.baheti@gmail.com.)</i></p>", unsafe_allow_html=True)

# Set smaller font size for subtitle
st.markdown("<h2 style='font-family:Raleway; font-size: 1.7rem;'>Top Topics Discussed</h2>", unsafe_allow_html=True)

# Year range slider
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.slider('Year Range Selection', min_value=min_year, max_value=max_year, value=(min_year, max_year), key='year_slider')  # Add key for shorter label

# Filter DataFrame based on selected year range
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Generate word cloud for top_0_words column
word_freq = {}
for index, row in filtered_df.iterrows():
    words_with_prob = eval(row['topic_0_words'])
    for word, prob in words_with_prob:
        word_freq[word] = word_freq.get(word, 0) + prob

# Create the word cloud
wordcloud = WordCloud(width=400, height=300, background_color='white', colormap='gist_earth').generate_from_frequencies(word_freq)

# Plot the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.image(wordcloud.to_array(), use_column_width=True)

# Define all_words
df['topic_0_words'] = df['topic_0_words'].apply(ast.literal_eval)
all_words = set(word for row in df['topic_0_words'] for word, _ in row)

st.markdown("<h2 style='font-family:Raleway; font-size: 1.7rem;'>Word Frequency Graph</h2>", unsafe_allow_html=True)

# Pre-select "covid" in the text input field
selected_word = st.text_input('Type a word:', 'covid')  # Pre-populate with "covid"

if selected_word:
    # Process the DataFrame to filter based on the typed word
    def filter_words(words_list, word):
        return [item for item in words_list if item[0] == word]

    df['filtered_words'] = df['topic_0_words'].apply(lambda x: filter_words(x, selected_word))
    df['sum_probabilities'] = df['filtered_words'].apply(lambda x: sum(prob for _, prob in x))

    # Check if there are any years with the selected word
    if df['sum_probabilities'].sum() > 0:
        fig, ax = plt.subplots()
        ax.plot(df['year'], df['sum_probabilities'], marker='o', linestyle='-', color='#524a4a', label='Frequency')

        # Set remaining plot properties and display the plot
        ax.set_xlabel('Year', fontname='Raleway')
        ax.set_ylabel('Sum of Probabilities', fontname='Raleway')
        ax.set_title(f'Frequency of "{selected_word}" over years')
        st.pyplot(fig)
    else:
        st.write(f'"{selected_word}" not found in the dataset for any year.')
