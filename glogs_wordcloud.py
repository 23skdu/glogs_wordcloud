#!/usr/bin/env python3
import os
import re
from collections import Counter
import argparse
from google.cloud import logging
from google.cloud import storage
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def setup_environment(project_id, credentials_path=None):
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    try:
        # Test connection.  If fails, usually means credentials or project ID issue
        logging_client = logging.Client()
        logging_client.list_entries(page_size=1)  # Small test
        print("Successfully connected to Google Cloud Logging.")
    except Exception as e:
        print(f"Error connecting to Google Cloud Logging: {e}")
        print("Please check your Project ID and credentials.")
        raise

def get_logs(project_id, log_name, num_entries, filter_string=None, order="timestamp desc"):
    """
    Args:
        project_id: Your Google Cloud Project ID.
        log_name: The name of the log to retrieve.  e.g., "projects/your-project-id/logs/your-log-name". Use 'global' for all logs
        num_entries: The number of log entries to retrieve.
        filter_string:  Optional filter string to apply to the logs (e.g., 'severity>=ERROR').
        order: The order in which to retrieve the logs (default: "timestamp desc").
    Returns:
        A list of log entry text payloads.  Returns an empty list if no logs found.
    """
    client = logging.Client(project=project_id)
    logger = client.logger(log_name)  # Use the actual log name
    log_filter = f'logName="{log_name}"'  #Crucial: filter by the specified log name.
    if filter_string:
        log_filter += f' AND ({filter_string})'
    entries = client.list_entries(
        page_size=num_entries,
        filter_=log_filter,
        order=order,
    )
    log_messages = []
    for entry in entries:
        try:
            # Try to extract the text payload directly, fallback to converting to JSON if not present
            if isinstance(entry.payload, str):
                log_messages.append(entry.payload)
            elif isinstance(entry.payload, dict):
                # Attempt to extract from a 'message' field if it exists
                if 'message' in entry.payload:
                    log_messages.append(entry.payload['message'])
                else:
                    log_messages.append(str(entry.payload)) #Convert to string to use
            else:
                log_messages.append(str(entry.payload)) #Convert to string to use if not a string or dict
        except Exception as e:
            print(f"Error processing log entry: {e}. Skipping.") #Handle potential errors and skip
            continue
    return log_messages

def clean_text(text):
    """
    Cleans the text by removing punctuation, converting to lowercase, and removing numbers.
    Args:
        text: The text to clean.
    Returns:
        The cleaned text.
    """
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\d+', '', text)  # Remove numbers
    return text


def analyze_word_frequency(log_messages, stop_words=None):
    """
    Analyzes the word frequency in a list of log messages.

    Args:
        log_messages: A list of log messages.
        stop_words: A set of stop words to exclude.

    Returns:
        A Counter object containing the word frequencies.
    """
    if stop_words is None:
        stop_words = set(STOPWORDS)

    word_counts = Counter()
    for message in log_messages:
        cleaned_message = clean_text(message)
        words = cleaned_message.split()
        words = [word for word in words if word not in stop_words and len(word) > 2]  # Remove short words
        word_counts.update(words)
    return word_counts

def analyze_phrase_frequency(log_messages, n=2, stop_words=None):
    """
    Analyzes the phrase frequency in a list of log messages.

    Args:
        log_messages: A list of log messages.
        n: The n-gram size (default: 2 for bigrams).
        stop_words: A set of stop words to exclude.

    Returns:
        A Counter object containing the phrase frequencies.
    """
    if stop_words is None:
        stop_words = set(STOPWORDS)

    phrase_counts = Counter()
    for message in log_messages:
        cleaned_message = clean_text(message)
        words = cleaned_message.split()
        words = [word for word in words if word not in stop_words and len(word) > 2]
        # Create n-grams (phrases)
        phrases = zip(*[words[i:] for i in range(n)])  # create tuples of n words
        phrases = [" ".join(phrase) for phrase in phrases] # Join the tuple into a string.
        phrase_counts.update(phrases)
    return phrase_counts

# --- Visualization ---

def generate_wordcloud(word_counts, output_file="wordcloud.png"):
    """
    Generates a word cloud from word frequencies and saves it to a file.

    Args:
        word_counts: A Counter object containing the word frequencies.
        output_file: The name of the output file.
    """
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=STOPWORDS,
        max_words=200,
        contour_width=3,
        contour_color="steelblue",
    ).generate_from_frequencies(word_counts)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(output_file)
    plt.show()
    print(f"Word cloud saved to {output_file}")

def main(project_id, log_name, num_entries, output_file="wordcloud.png", credentials_path=None, filter_string=None, analyze_phrases=False, ngram_size=2):
    """
    Main function to retrieve logs, analyze word/phrase frequency, and generate a word cloud.
    Args:
        project_id: Your Google Cloud Project ID.
        log_name: The name of the log to retrieve.
        num_entries: The number of log entries to retrieve.
        output_file: The name of the output file for the word cloud.
        credentials_path: Path to your service account key file (optional if using Application Default Credentials).
        filter_string: Optional filter string to apply to the logs (e.g., 'severity>=ERROR').
        analyze_phrases: Boolean flag to indicate if phrases should be analyzed instead of words.
        ngram_size: The n-gram size to use for phrase analysis.
    """
    try:
        setup_environment(project_id, credentials_path)
        log_messages = get_logs(project_id, log_name, num_entries, filter_string)
        if not log_messages:
            print("No log entries found.")
            return
        if analyze_phrases:
            phrase_counts = analyze_phrase_frequency(log_messages, n=ngram_size)
            generate_wordcloud(phrase_counts, output_file)
        else:
            word_counts = analyze_word_frequency(log_messages)
            generate_wordcloud(word_counts, output_file)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Google Cloud Logging data and generate a word cloud.")
    parser.add_argument("project_id", help="Your Google Cloud Project ID.")
    parser.add_argument("log_name", help="The name of the log to analyze (e.g., 'projects/your-project-id/logs/your-log-name'). Use 'global' for all logs")
    parser.add_argument("--num_entries", type=int, default=1000, help="The number of log entries to retrieve.")
    parser.add_argument("--output_file", type=str, default="wordcloud.png", help="The name of the output file for the word cloud.")
    parser.add_argument("--credentials_path", type=str, help="Path to your service account key file (optional).")
    parser.add_argument("--filter", type=str, help="Optional filter string (e.g., 'severity>=ERROR').")
    parser.add_argument("--analyze_phrases", action="store_true", help="Analyze phrases instead of single words.")
    parser.add_argument("--ngram_size", type=int, default=2, help="The n-gram size for phrase analysis (default: 2).")
    args = parser.parse_args()
    main(
        args.project_id,
        args.log_name,
        args.num_entries,
        args.output_file,
        args.credentials_path,
        args.filter,
        args.analyze_phrases,
        args.ngram_size
    )
