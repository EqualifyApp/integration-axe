


- [ ] Axe CLI Response Handling
- [ ] Send response to Rabbit
- [ ] Set up rabbit queue
- [ ] Set up queue to Postgres
- [ ] Set up Postgres inserter
- [ ]
- [ ]



Add to Prometheus Config File

scrape_configs:
  - job_name: 'Docker_Container_Name'
    static_configs:
      - targets: ['localhost:8083']
    metrics_path: '/metrics'

    Need to change localhost to container name or somethign like that - auto config type thing


    --##### Title



    def axe_scan(url):
    logger.debug(f'🌟 Starting to process: {url}')
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    # Create a Chrome driver instance
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)

    # Load the web page
    driver.get(url)

    # Run Axe
    axe = Axe(driver)
    axe.inject()
    results = axe.run()

    # Close the browser
    driver.quit()

    logger.info(f'✨ Results for {url}: {results}')

    # Send to Streamlining
    response = streamline_response(results)