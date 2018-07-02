# coding=UTF-8
from __future__ import division
import re

# This is a naive text summarization algorithm
# Created by Shlomi Babluki
# April, 2013


def split_content_to_sentences(content):
	content = content.replace("\n", ". ")
        return content.split(". ")

    # Naive method for splitting a text into paragraphs
def split_content_to_paragraphs(content):
	return content.split("\n\n")

    # Caculate the intersection between 2 sentences
def sentences_intersection(sent1, sent2):

        # split the sentence into words/tokens
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
def format_sentence(sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
def get_senteces_ranks(content):

      # Split the content into sentences
	sentences = split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[format_sentence(sentences[i])] = score
        return sentences_dic

def getkey(w):
	(a,b) = w
	return a
    # Return the best sentence in a paragraph
def get_best_sentence(paragraph, sentences_dic,l1):

        # Split the paragraph into sentences
	sentences = split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentences, temp = [], []
	for s in sentences:
            strip_s = format_sentence(s)
            if strip_s:
		temp += [(sentences_dic[strip_s],s)]
	temp = sorted(temp, reverse = True, key= getkey)
	d = min(l1, len(temp))	
	for i in range(d):
		(a,b) = temp[i]
		best_sentences += [b]
	return " ".join(best_sentences)

    # Main method, just run "python summary_tool.py"
def main():

    # Demo
    # Content from: "http://thenextweb.com/apps/2013/03/21/swayy-discover-curate-content/"

    content = input("Enter abstract")
    

    # Create a SummaryTool object
    
    # Build the sentences dictionary
    sentences_dic = get_senteces_ranks(content)

    # Build the summary with the sentences dictionary
    summary = get_best_sentence(content, sentences_dic)

    # Print the summary
    print summary

    # Print the ratio between the summary length and the original length
    #print ""
    #print "Original Length %s" % (len(title) + len(content))
    #print "Summary Length %s" % len(summary)
    #print "Summary Ratio: %s" % (100 - (100 * (len(summary) / (len(title) + len(content)))))


if __name__ == '__main__':
    main()
