from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords


def get_text_for_summaries(all_groups):
    all_text = []
    for number, group in enumerate(all_groups[:5]):
        text = []
        for count in range(len(group)):
            text.append((' '.join(word for word in group[count][0])) + '.')
        all_text.append(text)
        all_text[number] = ' '.join(word for word in all_text[number])
    return all_text


def get_summaries(all_text):
    summaries = []
    for s in range(len(all_text)):
        try:
            summary = summarize(all_text[s], word_count=40)
        except:
            summary = ''
        if summary == '':
            summaries.append(all_text[s][:150])
        else:
            summaries.append(summary)
    return summaries



'''
text_for_summaries = get_text_for_summaries(all_groups)

all_summaries = get_summaries(text_for_summaries)
'''
