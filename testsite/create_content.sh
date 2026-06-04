#!/bin/bash

NUM_POSTS=5
CONTENT_DIR=content
LOREM_API=https://jaspervdj.be/lorem-markdownum/markdown.txt

rm -fR content
mkdir -p content/images

for i in $(seq -w 1 ${NUM_POSTS})
do
    post_file=${CONTENT_DIR}/post${i}.markdown

    echo "Creating post ${i}"
    echo "Title: TEST_POST N ${i}" >> ${post_file}
    echo "Date: 2026-06-${i}" >> ${post_file}
    echo "Category: News" >> ${post_file}
    echo "Tags: news" >> ${post_file}
    echo "Summary: Summary of post ${i}" >> ${post_file}
    echo >> ${post_file}

    curl -s ${LOREM_API} | sed -r s,"^#","##", >> ${post_file}
done