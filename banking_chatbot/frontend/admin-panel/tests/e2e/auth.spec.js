import { test, expect } from '@playwright/test';

test.describe('Admin Panel Authentication Flow', () => {
  test('should successfully login with admin credentials and redirect to dashboard', async ({ page }) => {
    console.log('Starting authentication flow test...');
    
    // Step 1: Navigate to login page
    console.log('Step 1: Navigating to /login page...');
    await page.goto('/login');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Verify we're on the login page
    await expect(page).toHaveURL(/.*login/);
    console.log('✓ Successfully navigated to login page');
    
    // Step 2: Enter credentials
    console.log('Step 2: Entering credentials...');
    await page.fill('input[type="email"]', 'admin@joxai.com');
    await page.fill('input[type="password"]', 'admin123');
    console.log('✓ Credentials entered');
    
    // Step 3: Click login button
    console.log('Step 3: Clicking login button...');
    
    // Set up network request monitoring to verify API call
    const loginRequestPromise = page.waitForRequest(request => {
      return request.url().includes('/api/v1/auth/login') && request.method() === 'POST';
    });
    
    const loginResponsePromise = page.waitForResponse(response => {
      return response.url().includes('/api/v1/auth/login') && response.status() === 200;
    });
    
    await page.click('button[type="submit"]');
    
    // Wait for API call to complete
    try {
      const loginRequest = await loginRequestPromise;
      console.log('✓ Login API request sent:', loginRequest.url());
      
      const loginResponse = await loginResponsePromise;
      const responseData = await loginResponse.json();
      console.log('✓ Login API response received');
      console.log('  - Response status:', loginResponse.status());
      console.log('  - Token received:', !!responseData.token);
      console.log('  - User data:', responseData.user);
    } catch (error) {
      console.error('✗ Error during API call:', error);
      throw error;
    }
    
    // Step 4: Verify successful login
    console.log('Step 4: Verifying successful login...');
    
    // 4a: Check URL redirects to /dashboard
    await page.waitForURL(/.*dashboard/, { timeout: 5000 });
    await expect(page).toHaveURL(/.*dashboard/);
    console.log('✓ URL redirected to /dashboard');
    
    // 4b: Wait for dashboard to load
    await page.waitForLoadState('networkidle');
    console.log('✓ Dashboard page loaded');
    
    // 4c: Verify JWT token is stored in localStorage
    const token = await page.evaluate(() => localStorage.getItem('token'));
    expect(token).toBeTruthy();
    console.log('✓ JWT token stored in localStorage:', token ? token.substring(0, 20) + '...' : 'null');
    
    // 4d: Verify user data is stored in localStorage
    const userStr = await page.evaluate(() => localStorage.getItem('user'));
    expect(userStr).toBeTruthy();
    const user = JSON.parse(userStr);
    expect(user.email).toBe('admin@joxai.com');
    expect(user.role).toBe('admin');
    console.log('✓ User data stored correctly:', user);
    
    // 4e: Check if user information appears in header/sidebar
    // Wait for header or user info to be visible
    try {
      const headerVisible = await page.locator('.header, header, [class*="Header"]').first().isVisible({ timeout: 3000 });
      if (headerVisible) {
        console.log('✓ Header is visible');
      }
    } catch (e) {
      console.log('  Header element not found or not visible');
    }
    
    // Try to find user email or name in the page
    const pageContent = await page.content();
    if (pageContent.includes('admin@joxai.com') || pageContent.includes('Admin User')) {
      console.log('✓ User information appears on the page');
    } else {
      console.log('  User information not found in page content (may be in a different format)');
    }
    
    // 4f: Verify dashboard content (metrics/charts)
    try {
      // Look for common dashboard elements
      const metricsVisible = await page.locator('[class*="metric"], [class*="card"], [class*="chart"]').first().isVisible({ timeout: 3000 });
      if (metricsVisible) {
        console.log('✓ Dashboard metrics/charts are visible');
      }
    } catch (e) {
      console.log('  Dashboard metrics/charts not found (will verify in screenshot)');
    }
    
    // Step 5: Take screenshot of dashboard
    console.log('Step 5: Taking screenshot of dashboard...');
    await page.screenshot({ 
      path: 'banking_chatbot/frontend/admin-panel/tests/e2e/dashboard-after-login.png',
      fullPage: true 
    });
    console.log('✓ Screenshot saved to: tests/e2e/dashboard-after-login.png');
    
    console.log('\n=== Authentication Flow Test Completed Successfully ===');
  });
  
  test('should display error message with invalid credentials', async ({ page }) => {
    console.log('Testing login with invalid credentials...');
    
    await page.goto('/login');
    await page.waitForLoadState('networkidle');
    
    // Try to login with wrong credentials
    await page.fill('input[type="email"]', 'wrong@email.com');
    await page.fill('input[type="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');
    
    // Wait for error message
    const errorMessage = await page.locator('.error-message, [class*="error"]').first().textContent({ timeout: 5000 });
    expect(errorMessage).toBeTruthy();
    console.log('✓ Error message displayed:', errorMessage);
    
    // Verify we're still on login page
    await expect(page).toHaveURL(/.*login/);
    console.log('✓ User remains on login page after failed login');
  });
});
