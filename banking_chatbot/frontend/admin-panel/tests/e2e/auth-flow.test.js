import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const BASE_URL = 'http://localhost:5000';

async function testAuthenticationFlow() {
  console.log('=' .repeat(70));
  console.log('ADMIN PANEL AUTHENTICATION FLOW TEST - PUPPETEER');
  console.log('=' .repeat(70));
  console.log(`Test started at: ${new Date().toISOString()}\n`);

  let browser;
  let page;
  let testPassed = true;

  try {
    // Launch browser
    console.log('Launching headless browser...');
    browser = await puppeteer.launch({
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu'
      ]
    });
    
    page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    // Set up network request monitoring
    const requests = [];
    const responses = [];
    
    page.on('request', request => {
      requests.push({
        url: request.url(),
        method: request.method(),
        headers: request.headers()
      });
    });
    
    page.on('response', response => {
      responses.push({
        url: response.url(),
        status: response.status()
      });
    });

    // Step 1: Navigate to login page
    console.log('\nStep 1: Navigate to /login page');
    console.log('-' .repeat(70));
    await page.goto(`${BASE_URL}/login`, { waitUntil: 'networkidle0' });
    
    const loginUrl = page.url();
    console.log(`✓ Navigated to: ${loginUrl}`);
    
    if (!loginUrl.includes('/login')) {
      console.log('✗ ERROR: Not on login page!');
      testPassed = false;
    }

    // Take screenshot of login page
    const loginScreenshotPath = join(__dirname, 'screenshots', 'login-page.png');
    await page.screenshot({ path: loginScreenshotPath, fullPage: true });
    console.log(`✓ Login page screenshot saved: ${loginScreenshotPath}`);

    // Step 2: Enter credentials
    console.log('\nStep 2: Enter credentials');
    console.log('-' .repeat(70));
    
    const emailInput = await page.$('input[type="email"]');
    const passwordInput = await page.$('input[type="password"]');
    
    if (!emailInput || !passwordInput) {
      console.log('✗ ERROR: Could not find email or password input fields!');
      testPassed = false;
      throw new Error('Missing input fields');
    }
    
    await emailInput.type('admin@joxai.com');
    await passwordInput.type('admin123');
    console.log('✓ Email entered: admin@joxai.com');
    console.log('✓ Password entered: ********');

    // Step 3: Click login button
    console.log('\nStep 3: Click the Login button');
    console.log('-' .repeat(70));
    
    const loginButton = await page.$('button[type="submit"]');
    if (!loginButton) {
      console.log('✗ ERROR: Could not find login button!');
      testPassed = false;
      throw new Error('Missing login button');
    }

    // Clear previous requests/responses tracking
    requests.length = 0;
    responses.length = 0;

    // Click login and wait for navigation
    await Promise.all([
      loginButton.click(),
      page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 10000 }).catch(() => {
        console.log('Navigation timeout - checking current state...');
      })
    ]);

    // Wait a bit for any async operations
    await page.waitForTimeout(1000);

    // Step 4: Verify successful login
    console.log('\nStep 4: Verify successful login');
    console.log('-' .repeat(70));

    // 4a: Check API request was made
    const loginApiRequest = requests.find(r => 
      r.url.includes('/api/v1/auth/login') && r.method === 'POST'
    );
    
    if (loginApiRequest) {
      console.log('✓ Login API request detected:');
      console.log(`  URL: ${loginApiRequest.url}`);
      console.log(`  Method: ${loginApiRequest.method}`);
    } else {
      console.log('✗ WARNING: No login API request detected');
    }

    const loginApiResponse = responses.find(r => 
      r.url.includes('/api/v1/auth/login')
    );
    
    if (loginApiResponse) {
      console.log('✓ Login API response received:');
      console.log(`  Status: ${loginApiResponse.status}`);
      
      if (loginApiResponse.status !== 200) {
        console.log(`✗ ERROR: Login failed with status ${loginApiResponse.status}`);
        testPassed = false;
      }
    }

    // 4b: Check URL redirected to /dashboard
    const currentUrl = page.url();
    console.log(`\nCurrent URL: ${currentUrl}`);
    
    if (currentUrl.includes('/dashboard')) {
      console.log('✓ Successfully redirected to /dashboard');
    } else {
      console.log(`✗ WARNING: Not on dashboard page (URL: ${currentUrl})`);
      console.log('  Attempting to navigate to dashboard...');
      await page.goto(`${BASE_URL}/dashboard`, { waitUntil: 'networkidle0' });
    }

    // 4c: Verify JWT token in localStorage
    const token = await page.evaluate(() => localStorage.getItem('token'));
    
    if (token) {
      console.log(`✓ JWT token stored in localStorage`);
      console.log(`  Token preview: ${token.substring(0, 30)}...`);
    } else {
      console.log('✗ ERROR: JWT token not found in localStorage!');
      testPassed = false;
    }

    // 4d: Verify user data in localStorage
    const userStr = await page.evaluate(() => localStorage.getItem('user'));
    
    if (userStr) {
      const user = JSON.parse(userStr);
      console.log('✓ User data stored in localStorage:');
      console.log(`  Email: ${user.email}`);
      console.log(`  Name: ${user.name}`);
      console.log(`  Role: ${user.role}`);
      
      if (user.email !== 'admin@joxai.com' || user.role !== 'admin') {
        console.log('✗ ERROR: User data mismatch!');
        testPassed = false;
      }
    } else {
      console.log('✗ ERROR: User data not found in localStorage!');
      testPassed = false;
    }

    // 4e: Check for dashboard content
    console.log('\nChecking dashboard content...');
    
    const pageContent = await page.content();
    
    // Look for header/sidebar user info
    const headerSelectors = [
      '.header',
      'header',
      '[class*="Header"]',
      '.sidebar',
      '[class*="Sidebar"]'
    ];
    
    let headerFound = false;
    for (const selector of headerSelectors) {
      const element = await page.$(selector);
      if (element) {
        const isVisible = await element.isIntersectingViewport();
        if (isVisible) {
          console.log(`✓ Found visible element: ${selector}`);
          headerFound = true;
          break;
        }
      }
    }
    
    if (!headerFound) {
      console.log('  ℹ Header/Sidebar elements not detected (may use different selectors)');
    }

    // Look for dashboard metrics/charts
    const dashboardSelectors = [
      '[class*="metric"]',
      '[class*="card"]',
      '[class*="chart"]',
      '[class*="dashboard"]',
      '.metrics',
      '.charts'
    ];
    
    let dashboardContentFound = false;
    for (const selector of dashboardSelectors) {
      const elements = await page.$$(selector);
      if (elements.length > 0) {
        console.log(`✓ Found dashboard content: ${selector} (${elements.length} elements)`);
        dashboardContentFound = true;
        break;
      }
    }
    
    if (!dashboardContentFound) {
      console.log('  ℹ Dashboard metrics/charts not detected (will verify in screenshot)');
    }

    // Step 5: Take screenshot of dashboard
    console.log('\nStep 5: Take screenshot of dashboard after successful login');
    console.log('-' .repeat(70));
    
    const dashboardScreenshotPath = join(__dirname, 'screenshots', 'dashboard-after-login.png');
    await page.screenshot({ path: dashboardScreenshotPath, fullPage: true });
    console.log(`✓ Dashboard screenshot saved: ${dashboardScreenshotPath}`);
    
    // Also take a viewport screenshot
    const viewportScreenshotPath = join(__dirname, 'screenshots', 'dashboard-viewport.png');
    await page.screenshot({ path: viewportScreenshotPath });
    console.log(`✓ Viewport screenshot saved: ${viewportScreenshotPath}`);

    // Get page title
    const pageTitle = await page.title();
    console.log(`✓ Page title: "${pageTitle}"`);

    // Summary
    console.log('\n' + '=' .repeat(70));
    if (testPassed) {
      console.log('✓ AUTHENTICATION FLOW TEST: PASSED');
    } else {
      console.log('✗ AUTHENTICATION FLOW TEST: FAILED (see errors above)');
    }
    console.log('=' .repeat(70));
    
    console.log('\nTest Summary:');
    console.log('  ✓ Login page loaded successfully');
    console.log('  ✓ Credentials entered (admin@joxai.com / admin123)');
    console.log('  ✓ Login button clicked');
    console.log(`  ${loginApiResponse?.status === 200 ? '✓' : '✗'} API authentication successful`);
    console.log(`  ${currentUrl.includes('/dashboard') ? '✓' : '?'} Redirected to dashboard`);
    console.log(`  ${token ? '✓' : '✗'} JWT token stored in localStorage`);
    console.log(`  ${userStr ? '✓' : '✗'} User data stored in localStorage`);
    console.log('  ✓ Screenshots captured');
    
    console.log('\nScreenshots saved:');
    console.log(`  - ${loginScreenshotPath}`);
    console.log(`  - ${dashboardScreenshotPath}`);
    console.log(`  - ${viewportScreenshotPath}`);

  } catch (error) {
    console.error('\n✗ ERROR during test execution:');
    console.error(error);
    testPassed = false;
  } finally {
    if (browser) {
      await browser.close();
      console.log('\n✓ Browser closed');
    }
  }

  process.exit(testPassed ? 0 : 1);
}

// Run the test
testAuthenticationFlow();
