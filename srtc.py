import asyncio
import aiohttp
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from tqdm import tqdm

CONCURRENT_REQUESTS_PER_URL = 32
TOTAL_REQUESTS_PER_URL = 1000

async def fetch(sem, session, url, results):
    async with sem:
        start_time = time.time()
        try:
            async with session.get(url) as response:
                status = response.status
        except Exception as e:
            # If there is an error, record it as a 500 status
            status = 500
        end_time = time.time()
        response_time = end_time - start_time
    results[url].append((status, response_time))

async def main(url1, url2):
    urls = {"Base": url1, "New/Change": url2}
    results = {url1: [], url2: []}

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls.values():
            sem = asyncio.Semaphore(CONCURRENT_REQUESTS_PER_URL)
            for _ in range(TOTAL_REQUESTS_PER_URL):
                task = fetch(sem, session, url, results)
                tasks.append(task)
        for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=f"Processing tasks"):
            await f

    fig, axs = plt.subplots(2, 2, figsize=(20, 11.25))
    axs = axs.flatten()
    comparison_data = []
    no_errors = True

    for ax, (url_name, data) in zip(axs[:2], zip(urls.keys(), results.values())):
        status_codes, times = zip(*data)
        times = np.array(times) * 1000  # convert to milliseconds
        success_times = times[np.array(status_codes) < 400]  # consider status codes below 400 as successes

        ax.hist(success_times, bins=50, color=(80/255, 158/255, 47/255), edgecolor='black')
        ax.set_title(f'Response times for {url_name}')
        ax.set_xlabel('Response time (ms)')
        ax.set_ylabel('Frequency')

        avg_response_time = np.mean(success_times)
        avg_response_time_display = f'{avg_response_time:.2f} ms' if avg_response_time < 1000 else f'{avg_response_time/1000:.2f} s'
        error_percent = 100 * (len(times) - len(success_times)) / len(times)
        if error_percent > 0:
            no_errors = False
        ax.text(0.6, 0.85, f'Average response time: {avg_response_time_display}\nError percentage: {error_percent:.2f}%', transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black'))

        comparison_data.append((avg_response_time, error_percent))

    # comparison plot for average response times
    avg_times = [data[0] for data in comparison_data]
    bars = axs[2].bar(urls.keys(), avg_times, color=(80/255, 158/255, 47/255), edgecolor='black')
    axs[2].set_title('Average response times comparison')
    axs[2].set_ylabel('Response time (ms)')
    for bar, avg_time in zip(bars, avg_times):
        height = bar.get_height()
        performance = (avg_times[1] - avg_time) / avg_times[1] * 100
        axs[2].text(bar.get_x() + bar.get_width() / 2, height, f'{performance:+.1f}%', ha='center', va='bottom', fontweight='bold')

    # comparison plot for error percentages
    if no_errors:
        axs[3].text(0.5, 0.5, 'No Errors Found', ha='center', va='center', fontsize=20)
        axs[3].axis('off')
    else:
        axs[3].bar(urls.keys(), [data[1] for data in comparison_data], color=(243/255, 23/255, 58/255), edgecolor='black')
        axs[3].set_title('Error percentages comparison')
        axs[3].set_ylabel('Error percentage (%)')

    plt.text(0.99, 0.01, 'github.com/stanislavromanov', ha='right', va='bottom', fontsize=10, color='gray', transform=plt.gcf().transFigure)

    # Add the logo to the plot beside the credits line
    # logo = mpimg.imread('logo.png')
    # figlogo = fig.add_axes([0.01, 0.01, 165/1920, 30/1080], anchor='SW')
    # figlogo.imshow(logo)
    # figlogo.axis('off')

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.2, hspace=0.3)
    plt.savefig('comparison_graph.png')

if __name__ == '__main__':
    import sys
    url1, url2 = sys.argv[1], sys.argv[2]
    asyncio.run(main(url1, url2))
