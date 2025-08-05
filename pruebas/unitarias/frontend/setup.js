// Setup file for Jest tests
// This file is executed before each test file

const Dashboard = require('./dashboard-test-component.js');
const Auth = require('./auth-test-component.js');
const Pet = require('./pet-test-component.js');

// Make components available globally
global.Dashboard = Dashboard;
global.Auth = Auth;
global.Pet = Pet;

// Mock global objects that are available in the browser
global.localStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn()
};

global.sessionStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn()
};

// Mock fetch API
// Mock Date for consistent testing
const RealDate = global.Date;
const mockDate = new RealDate('2024-01-15T10:00:00Z');

global.Date = class extends RealDate {
    constructor(...args) {
        if (args.length === 0) {
            super(mockDate.getTime());
        } else {
            super(...args);
        }
    }
    
    static now() {
        return mockDate.getTime();
    }
    
    static parse(dateString) {
        return RealDate.parse(dateString);
    }
    
    static UTC(...args) {
        return RealDate.UTC(...args);
    }
};

global.fetch = jest.fn();

// Mock console methods to reduce noise in tests
global.console = {
  ...console,
  log: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  info: jest.fn()
};

// Mock window object
try {
  Object.defineProperty(window, 'location', {
    value: {
      href: 'http://localhost:3000',
      origin: 'http://localhost:3000'
    },
    writable: true,
    configurable: true
  });
} catch (e) {
  // If location is already defined, just modify it
  window.location = {
    href: 'http://localhost:3000',
    origin: 'http://localhost:3000'
  };
}

// Reset all mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
  
  // Reset fetch
  fetch.mockClear();
});

// Add custom matchers if needed
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    if (pass) {
      return {
        message: () =>
          `expected ${received} not to be within range ${floor} - ${ceiling}`,
        pass: true,
      };
    } else {
      return {
        message: () =>
          `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false,
      };
    }
  },
});
