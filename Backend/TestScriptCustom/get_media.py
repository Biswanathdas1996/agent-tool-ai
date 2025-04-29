import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def get_media_from_url(html_content, base_url=''):
    try:
        
        soup = BeautifulSoup(html_content, 'html.parser')

        images = []
        videos = []
        attachments = []

        # Get all <img> tags
        for img_tag in soup.find_all('img'):
            img_url = img_tag.get('src')
            if img_url:
                full_img_url = urljoin(base_url, img_url)  # handle relative URLs
                images.append(full_img_url)

        # Get all <video> and <source> tags
        for video_tag in soup.find_all(['video', 'source']):
            video_url = video_tag.get('src')
            if video_url:
                full_video_url = urljoin(base_url, video_url)
                videos.append(full_video_url)

        # Get all <a> tags for file attachments
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.lower().endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar', '.ppt', '.pptx')):
                full_attachment_url = urljoin(base_url, href)
                attachments.append(full_attachment_url)

        media = {
            'images': images,
            'videos': videos,
            'attachments': attachments
        }
        
        return media

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None


