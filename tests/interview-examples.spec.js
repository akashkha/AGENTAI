const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

const tempFilePath = path.join(__dirname, 'test-file.txt');

// 1. Demonstrates how to handle alerts
test('handling JavaScript alerts', async ({ page }) => {
    await page.goto('https://the-internet.herokuapp.com/javascript_alerts');
    
    // Setup listener for dialog
    page.on('dialog', async dialog => {
        expect(dialog.type()).toBe('alert');
        expect(dialog.message()).toBe('I am a JS Alert');
        await dialog.accept();
    });
    
    await page.locator('button[onclick="jsAlert()"]').click();
    expect(await page.locator('#result').textContent()).toBe('You successfully clicked an alert');
});

// 2. Demonstrates handling dynamic elements and waits
test('handling dynamic loading', async ({ page }) => {
    await page.goto('https://the-internet.herokuapp.com/dynamic_loading/1');
    
    await page.locator('button').click();
    await page.waitForSelector('#loading');
    await page.waitForSelector('#finish h4', { state: 'visible' });
    
    const finishText = await page.locator('#finish h4').textContent();
    expect(finishText).toBe('Hello World!');
});

// 3. Demonstrates file upload handling
test('handling file uploads', async ({ page }) => {
    // Create test directory if it doesn't exist
    const testDir = path.dirname(tempFilePath);
    if (!fs.existsSync(testDir)) {
        fs.mkdirSync(testDir, { recursive: true });
    }
    
    // Create test file before test
    try {
        fs.writeFileSync(tempFilePath, 'Test file content');
    } catch (error) {
        console.error('Error creating temp file:', error);
        throw error;
    }
    
    await page.goto('https://the-internet.herokuapp.com/upload');
    
    // Use file chooser to upload temp file
    await page.setInputFiles('#file-upload', tempFilePath);
    await page.locator('#file-submit').click();
    
    expect(await page.locator('.example h3').textContent()).toBe('File Uploaded!');
});

// 4. Demonstrates handling iframes and frames
test('working with frames', async ({ page }) => {
    // Go to a page with nested frames
    await page.goto('https://the-internet.herokuapp.com/nested_frames');
    
    // Check top frame content
    const topFrame = page.frameLocator('frame[name="frame-top"]');
    
    // Verify left frame
    const leftFrame = topFrame.frameLocator('frame[name="frame-left"]');
    const leftText = await leftFrame.locator('body').textContent();
    expect(leftText.trim()).toBe('LEFT');
    
    // Verify middle frame
    const middleFrame = topFrame.frameLocator('frame[name="frame-middle"]');
    const middleText = await middleFrame.locator('body').textContent();
    expect(middleText.trim()).toBe('MIDDLE');
    
    // Verify right frame
    const rightFrame = topFrame.frameLocator('frame[name="frame-right"]');
    const rightText = await rightFrame.locator('body').textContent();
    expect(rightText.trim()).toBe('RIGHT');
    
    // Verify bottom frame
    const bottomFrame = page.frameLocator('frame[name="frame-bottom"]');
    const bottomText = await bottomFrame.locator('body').textContent();
    expect(bottomText.trim()).toBe('BOTTOM');
});

// 5. Demonstrates handling multiple windows/tabs
test('handling multiple windows', async ({ context }) => {
    const page = await context.newPage();
    await page.goto('https://the-internet.herokuapp.com/windows');
    
    // Create a promise to handle new page
    const [newPage] = await Promise.all([
        context.waitForEvent('page'),
        page.click('a[href="/windows/new"]')
    ]);
    
    await newPage.waitForLoadState();
    expect(await newPage.textContent('h3')).toBe('New Window');
});

// 6. Demonstrates API testing
test('API testing example', async ({ request }) => {
    const response = await request.get('https://jsonplaceholder.typicode.com/posts/1');
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(body.id).toBe(1);
    expect(body.title).toBeTruthy();
});

// 7. Demonstrates data-driven testing
const testData = [
    { username: 'invalid1', password: 'pass1', expected: 'Your username is invalid!' },
    { username: 'invalid2', password: 'pass2', expected: 'Your username is invalid!' },
    { username: 'tomsmith', password: 'SuperSecretPassword!', expected: 'You logged into a secure area!' }
];

for (const data of testData) {
    test(`login test with ${data.username}`, async ({ page }) => {
        await page.goto('https://the-internet.herokuapp.com/login');
        
        await page.fill('#username', data.username);
        await page.fill('#password', data.password);
        await page.click('button[type="submit"]');
        
        const message = await page.locator('#flash').textContent();
        expect(message).toContain(data.expected);
    });
}

// 8. Demonstrates basic visual comparison
test('basic visual test example', async ({ page }) => {
    await page.goto('https://example.com');
    await page.waitForLoadState('domcontentloaded');
    
    const heading = await page.locator('h1');
    expect(await heading.textContent()).toBe('Example Domain');
    expect(await heading.isVisible()).toBeTruthy();
});

// 9. Demonstrates element state handling
test('element state handling', async ({ page }) => {
    await page.goto('https://the-internet.herokuapp.com/dynamic_controls');
    
    // Test checkbox functionality
    const checkbox = page.locator('input[type="checkbox"]');
    await expect(checkbox).toBeVisible();
    await checkbox.check();
    expect(await checkbox.isChecked()).toBeTruthy();
    
    // Test enable/disable functionality
    const enableButton = page.locator('button:has-text("Enable")');
    await enableButton.click();
    await page.waitForSelector('input[type="text"]:not([disabled])');
    const input = page.locator('input[type="text"]');
    expect(await input.isEnabled()).toBeTruthy();
});

// 10. Demonstrates performance testing
test('basic performance check', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('https://example.com');
    await page.waitForLoadState('domcontentloaded');
    
    const loadTime = Date.now() - startTime;
    console.log(`Page load time: ${loadTime}ms`);
    
    // More lenient timeout for CI environments
    expect(loadTime).toBeLessThan(10000);
});

// Cleanup temp file after tests
test.afterAll(async () => {
    try {
        if (fs.existsSync(tempFilePath)) {
            fs.unlinkSync(tempFilePath);
        }
    } catch (error) {
        console.log('Error cleaning up temp file:', error);
    }
});