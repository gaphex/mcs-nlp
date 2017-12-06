import os
import yaml
import base64
import logging
import asyncio
import aiohttp
import numpy as np
import async_timeout
import subprocess

from config import DL_DIR, GSR_CONFIG
from scipy.io import wavfile

gsr_params = yaml.load(open("gsr_config.yml"))

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Logging to console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


async def post_json(sem, session, url, json=None, params=None, timeout=5 * 60, ignore_exception=True):
    try:
        async with sem:
            async with session.post(url, json=json, params=params, timeout=timeout) as response:
                response_data = await response.json()
    except Exception as e:
        response_data = dict(error=1, message='post_json error: {}'.format(str(e)))

    return response_data

async def google_transcribe(wav, asr_options):
    
    sem = asyncio.BoundedSemaphore(4)
    session = aiohttp.ClientSession()

    audio_content = base64.b64encode(wav.tobytes()).decode("utf8")
    ret = await post_json(
        sem, session, asr_options['URL'],
        json=dict(
            audio=dict(content=audio_content),
            config=asr_options['CONFIG'],
        ),
        params=dict(key=asr_options.get('KEY')),
        timeout=asr_options['TIMEOUT'],
    )
    if 'results' in ret:
        text = ret['results'][0]['alternatives'][0]['transcript']
    else:
        text = 'unrecognized'
        
    await session.close()
    return text

def convert_to_wav16b16k(in_filename, out_filename):

    command = ['ffmpeg','-i', in_filename,'-ar', '16000', out_filename]
    proc = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return out_filename

def speech2text(ogg_file):
    
    wav_file = convert_to_wav16b16k(ogg_file, "{}/{}.wav".format(DL_DIR, np.random.randint(0, 10000)))
    logger.info("converted to wav")
    try:
        task = asyncio.ensure_future(google_transcribe(wavfile.read(wav_file)[1], gsr_params))
        text = asyncio.get_event_loop().run_until_complete(task)
    except Exception as e:
        logger.warn(e)
        
    logger.info("transcribed")
    os.remove(wav_file)
    logger.info("tmp file {} removed".format(wav_file))
    return text