import subprocess
import time

def run_spiders_parallel():
    """Run multiple Scrapy spiders in parallel"""
    spiders = ["books", "docs_sitemap", "encyclopedia_rss", "forum_rss", "news_rss"]

    print(f"Starting {len(spiders)} spiders in parallel...")

    processes = []
    for spider in spiders:
        print(f"Starting spider: {spider}")
        cmd = ["python", "-m", "scrapy", "crawl", spider]
        proc = subprocess.Popen(cmd)
        processes.append((spider, proc))
        time.sleep(2)  # Stagger the start times slightly

    print("All spiders started. Waiting for completion...")

    # Wait for all processes to complete
    for spider_name, proc in processes:
        print(f"Waiting for {spider_name} to complete...")
        proc.wait()  # Wait for this process to finish
        if proc.returncode == 0:
            print(f"✓ {spider_name} completed successfully")
        else:
            print(f"✗ {spider_name} failed with return code {proc.returncode}")

    print("All spiders completed!")

if __name__ == "__main__":
    run_spiders_parallel()
