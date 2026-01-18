const state = {
  token: localStorage.getItem('adminToken') || '',
  user: null,
  activity: [],
  cms: {
    current: null,
    data: null,
    draft: null,
  },
  news: {
    page: 1,
    pageSize: 10,
    total: 0,
  },
  assets: {
    page: 1,
    pageSize: 12,
    total: 0,
  },
  assetPicker: {
    open: false,
    page: 1,
    pageSize: 24,
    totalPages: 1,
    search: '',
    items: [],
    onSelect: null,
  },
};

const rootPath = (() => {
  const path = window.location.pathname;
  const idx = path.indexOf('/admin');
  if (idx === -1) {
    return '';
  }
  return path.slice(0, idx);
})();

const API_BASE = rootPath;

const elements = {
  loginView: document.getElementById('loginView'),
  loginForm: document.getElementById('loginForm'),
  loginUsername: document.getElementById('loginUsername'),
  loginPassword: document.getElementById('loginPassword'),
  loginHint: document.getElementById('loginHint'),
  appView: document.getElementById('appView'),
  logoutBtn: document.getElementById('logoutBtn'),
  currentUser: document.getElementById('currentUser'),
  refreshBtn: document.getElementById('refreshBtn'),
  viewTitle: document.getElementById('viewTitle'),
  viewSubtitle: document.getElementById('viewSubtitle'),
  envPill: document.getElementById('envPill'),
  toast: document.getElementById('toast'),
  healthStatus: document.getElementById('healthStatus'),
  healthMeta: document.getElementById('healthMeta'),
  newsCount: document.getElementById('newsCount'),
  assetCount: document.getElementById('assetCount'),
  activityFeed: document.getElementById('activityFeed'),
  cmsSectionList: document.getElementById('cmsSectionList'),
  cmsSectionTitle: document.getElementById('cmsSectionTitle'),
  cmsSectionHint: document.getElementById('cmsSectionHint'),
  cmsForm: document.getElementById('cmsForm'),
  cmsAdvanced: document.getElementById('cmsAdvanced'),
  cmsEditor: document.getElementById('cmsEditor'),
  cmsLoadBtn: document.getElementById('cmsLoadBtn'),
  cmsSaveBtn: document.getElementById('cmsSaveBtn'),
  newsTableBody: document.querySelector('#newsTable tbody'),
  newsPagination: document.getElementById('newsPagination'),
  newsReloadBtn: document.getElementById('newsReloadBtn'),
  newsNewBtn: document.getElementById('newsNewBtn'),
  newsFormTitle: document.getElementById('newsFormTitle'),
  newsForm: document.getElementById('newsForm'),
  newsId: document.getElementById('newsId'),
  newsTitle: document.getElementById('newsTitle'),
  newsSlug: document.getElementById('newsSlug'),
  newsCategory: document.getElementById('newsCategory'),
  newsAuthor: document.getElementById('newsAuthor'),
  newsCover: document.getElementById('newsCover'),
  newsTags: document.getElementById('newsTags'),
  newsSummary: document.getElementById('newsSummary'),
  newsContent: document.getElementById('newsContent'),
  newsMetaTitle: document.getElementById('newsMetaTitle'),
  newsMetaDescription: document.getElementById('newsMetaDescription'),
  newsPublished: document.getElementById('newsPublished'),
  newsPublishedAt: document.getElementById('newsPublishedAt'),
  newsStatusFilter: document.getElementById('newsStatusFilter'),
  newsCategoryFilter: document.getElementById('newsCategoryFilter'),
  newsApplyFilter: document.getElementById('newsApplyFilter'),
  newsResetBtn: document.getElementById('newsResetBtn'),
  assetUploadForm: document.getElementById('assetUploadForm'),
  assetFile: document.getElementById('assetFile'),
  assetCategory: document.getElementById('assetCategory'),
  assetAltText: document.getElementById('assetAltText'),
  assetGrid: document.getElementById('assetGrid'),
  assetPagination: document.getElementById('assetPagination'),
  assetReloadBtn: document.getElementById('assetReloadBtn'),
  apiBase: document.getElementById('apiBase'),
  envValue: document.getElementById('envValue'),

  assetPicker: document.getElementById('assetPicker'),
  assetPickerClose: document.getElementById('assetPickerClose'),
  assetPickerSearch: document.getElementById('assetPickerSearch'),
  assetPickerReload: document.getElementById('assetPickerReload'),
  assetPickerGrid: document.getElementById('assetPickerGrid'),
  assetPickerPagination: document.getElementById('assetPickerPagination'),
};

const cmsSections = [
  { id: 'home', name: 'Home (Aggregated)', endpoint: '/api/v1/cms/home', readonly: true },
  { id: 'site-branding', name: 'Site Branding', endpoint: '/api/v1/cms/site-branding' },
  { id: 'header', name: 'Header', endpoint: '/api/v1/cms/header' },
  { id: 'hero', name: 'Hero', endpoint: '/api/v1/cms/hero' },
  { id: 'about', name: 'About', endpoint: '/api/v1/cms/about' },
  { id: 'services', name: 'Services', endpoint: '/api/v1/cms/services' },
  { id: 'stats', name: 'Stats', endpoint: '/api/v1/cms/stats' },
  { id: 'testimonials', name: 'Testimonials', endpoint: '/api/v1/cms/testimonials' },
  { id: 'gallery', name: 'Gallery', endpoint: '/api/v1/cms/gallery' },
  { id: 'footer', name: 'Footer', endpoint: '/api/v1/cms/footer' },
  { id: 'seo', name: 'SEO', endpoint: '/api/v1/cms/seo' },
  { id: 'offers', name: 'Offers', endpoint: '/api/v1/cms/offers' },
  { id: 'popular-dishes', name: 'Popular Dishes', endpoint: '/api/v1/cms/popular-dishes' },
  { id: 'cta', name: 'CTA', endpoint: '/api/v1/cms/cta' },
  { id: 'food-menu', name: 'Food Menu', endpoint: '/api/v1/cms/food-menu' },
  { id: 'special-offer', name: 'Special Offer', endpoint: '/api/v1/cms/special-offer' },
  { id: 'chef', name: 'Chef', endpoint: '/api/v1/cms/chef' },
  { id: 'client-logos', name: 'Client Logos', endpoint: '/api/v1/cms/client-logos' },
];

function fieldText(key, label, placeholder = '', opts = {}) {
  return { type: 'text', key, label, placeholder, ...opts };
}

function fieldTextarea(key, label, placeholder = '', opts = {}) {
  return { type: 'textarea', key, label, placeholder, full: true, ...opts };
}

function fieldNumber(key, label, opts = {}) {
  return { type: 'number', key, label, ...opts };
}

function fieldBoolean(key, label, opts = {}) {
  return { type: 'boolean', key, label, full: true, ...opts };
}

function fieldImage(key, label, opts = {}) {
  return { type: 'image', key, label, full: true, ...opts };
}

function fieldKeyValue(key, label, opts = {}) {
  return { type: 'keyvalue', key, label, full: true, ...opts };
}

function fieldNav(key, label, opts = {}) {
  return { type: 'nav', key, label, full: true, ...opts };
}

function fieldArray(key, label, itemDef, defaultItem, opts = {}) {
  return {
    type: 'array',
    key,
    label,
    full: true,
    item: itemDef,
    defaultItem,
    ...opts,
  };
}

function fieldArrayObjects(key, label, itemLabel, itemFields, defaultItem, opts = {}) {
  return {
    type: 'array',
    key,
    label,
    full: true,
    itemLabel,
    itemFields,
    defaultItem,
    ...opts,
  };
}

const SOCIAL_PRESETS = [
  'facebook',
  'instagram',
  'twitter',
  'linkedin',
  'youtube',
  'tiktok',
  'whatsapp',
];

const cmsFormConfigs = {
  'site-branding': {
    groups: [
      { title: 'Brand', columns: 2, fields: [fieldText('company_name', 'Company Name'), fieldText('tagline', 'Tagline')] },
      {
        title: 'Images',
        columns: 2,
        fields: [
          fieldImage('logo_image_path', 'Logo (Dark)'),
          fieldImage('logo_white_image_path', 'Logo (White)'),
          fieldImage('favicon_path', 'Favicon'),
        ],
      },
    ],
  },
  header: {
    groups: [
      {
        title: 'Header Settings',
        columns: 2,
        fields: [
          fieldText('operating_hours', 'Operating Hours', '09:00 am - 06:00 pm'),
          fieldText('cta_text', 'CTA Text', 'ORDER NOW'),
          fieldText('cta_link', 'CTA Link', '/menu'),
        ],
      },
      { title: 'Navigation', columns: 1, fields: [fieldNav('nav_items', 'Navigation Menu')] },
      { title: 'Social Links', columns: 1, fields: [fieldKeyValue('social_links', 'Social Links', { presets: SOCIAL_PRESETS })] },
      {
        title: 'Sidebar / Contact',
        columns: 2,
        fields: [
          fieldTextarea('sidebar_description', 'Sidebar Description'),
          fieldText('contact_address', 'Address'),
          fieldText('contact_email', 'Email'),
          fieldText('contact_phone', 'Phone'),
          fieldText('contact_hours', 'Contact Hours'),
        ],
      },
      {
        title: 'Offcanvas Gallery Images',
        columns: 1,
        fields: [
          fieldArray(
            'offcanvas_gallery_images',
            'Images',
            { type: 'image', label: 'Image' },
            () => null,
          ),
        ],
      },
    ],
  },
  hero: {
    groups: [
      {
        title: 'Slides',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'slides',
            'Slides',
            'Slide',
            [
              fieldText('subtitle', 'Subtitle'),
              fieldText('title', 'Title', 'Fresh & Tasty'),
              fieldText('cta_text', 'CTA Text', 'ORDER NOW'),
              fieldText('cta_link', 'CTA Link', '/menu'),
              fieldImage('image_path', 'Slide Image'),
              fieldImage('background_image_path', 'Background Image'),
            ],
            () => ({
              subtitle: null,
              title: 'New Slide',
              cta_text: 'ORDER NOW',
              cta_link: '/menu',
              image_path: null,
              background_image_path: null,
            }),
          ),
        ],
      },
      {
        title: 'Shape Images',
        columns: 1,
        fields: [fieldArray('shape_images', 'Images', { type: 'image', label: 'Image' }, () => null)],
      },
    ],
  },
  about: {
    groups: [
      { title: 'Heading', columns: 2, fields: [fieldText('section_subtitle', 'Subtitle'), fieldText('section_title', 'Title')] },
      { title: 'Content', columns: 1, fields: [fieldTextarea('description', 'Description')] },
      { title: 'Highlights', columns: 1, fields: [fieldArray('highlight_points', 'Points', { type: 'text', label: 'Point' }, () => '')] },
      { title: 'CTA', columns: 2, fields: [fieldText('cta_text', 'CTA Text', 'ORDER NOW'), fieldText('cta_link', 'CTA Link', '/menu')] },
      {
        title: 'Images',
        columns: 1,
        fields: [
          fieldImage('background_image_path', 'Background Image'),
          fieldArray('shape_images', 'Shape Images', { type: 'image', label: 'Image' }, () => null),
        ],
      },
    ],
  },
  services: {
    groups: [
      { title: 'Heading', columns: 2, fields: [fieldText('section_subtitle', 'Subtitle'), fieldText('section_title', 'Title')] },
      {
        title: 'Items',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'items',
            'Service Items',
            'Item',
            [
              fieldText('name', 'Name', 'New Item'),
              fieldTextarea('description', 'Description'),
              fieldText('price', 'Price', '$0'),
              fieldText('link', 'Link', '/menu'),
              fieldImage('image_path', 'Image'),
            ],
            () => ({
              name: 'New Item',
              description: null,
              price: null,
              image_path: null,
              link: null,
            }),
          ),
        ],
      },
    ],
  },
  stats: {
    groups: [
      {
        title: 'Stats',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'items',
            'Stats',
            'Stat',
            [fieldText('label', 'Label', 'Happy Customers'), fieldText('value', 'Value', '0'), fieldText('icon', 'Icon', 'users')],
            () => ({ label: 'New Stat', value: '0', icon: null }),
          ),
        ],
      },
      { title: 'Background', columns: 1, fields: [fieldImage('background_image_path', 'Background Image')] },
    ],
  },
  testimonials: {
    groups: [
      { title: 'Heading', columns: 2, fields: [fieldText('section_subtitle', 'Subtitle'), fieldText('section_title', 'Title')] },
      {
        title: 'Video',
        columns: 2,
        fields: [fieldText('video_url', 'Video URL'), fieldImage('video_thumbnail_path', 'Video Thumbnail')],
      },
      { title: 'Background', columns: 1, fields: [fieldImage('background_image_path', 'Background Image')] },
      {
        title: 'Testimonials',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'items',
            'Testimonials',
            'Testimonial',
            [
              fieldText('name', 'Name', 'Customer'),
              fieldText('role', 'Role', 'Guest'),
              fieldTextarea('message', 'Message'),
              fieldImage('avatar_path', 'Avatar'),
              fieldNumber('rating', 'Rating (1-5)', { min: 1, max: 5, step: 1 }),
            ],
            () => ({ name: 'Customer', role: null, message: 'Great food!', avatar_path: null, rating: 5 }),
          ),
        ],
      },
    ],
  },
  gallery: {
    groups: [
      {
        title: 'Gallery Images',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'images',
            'Images',
            'Image',
            [fieldImage('image_path', 'Image'), fieldText('caption', 'Caption'), fieldText('link', 'Link')],
            () => ({ image_path: '', caption: null, link: null }),
          ),
        ],
      },
    ],
  },
  footer: {
    groups: [
      {
        title: 'Contact',
        columns: 2,
        fields: [fieldText('address', 'Address'), fieldText('phone', 'Phone'), fieldText('email', 'Email')],
      },
      { title: 'Description', columns: 1, fields: [fieldTextarea('description', 'Footer Description')] },
      { title: 'Social Links', columns: 1, fields: [fieldKeyValue('social_links', 'Social Links', { presets: SOCIAL_PRESETS })] },
      {
        title: 'Links',
        columns: 1,
        fields: [
          fieldArrayObjects('quick_links', 'Quick Links', 'Link', [fieldText('label', 'Label'), fieldText('link', 'Link')], () => ({ label: 'New Link', link: '/' })),
          fieldArrayObjects('menu_links', 'Menu Links', 'Link', [fieldText('label', 'Label'), fieldText('link', 'Link')], () => ({ label: 'New Link', link: '/' })),
        ],
      },
      { title: 'Hours', columns: 2, fields: [fieldText('weekday_hours', 'Weekday Hours'), fieldText('saturday_hours', 'Saturday Hours')] },
      {
        title: 'Legal',
        columns: 2,
        fields: [
          fieldText('copyright_text', 'Copyright Text'),
          fieldText('terms_link', 'Terms Link'),
          fieldText('privacy_link', 'Privacy Link'),
          fieldBoolean('newsletter_enabled', 'Enable Newsletter'),
        ],
      },
    ],
  },
  seo: {
    groups: [
      { title: 'Meta', columns: 2, fields: [fieldText('meta_title', 'Meta Title'), fieldTextarea('meta_description', 'Meta Description'), fieldTextarea('meta_keywords', 'Meta Keywords')] },
      { title: 'Open Graph', columns: 2, fields: [fieldText('og_title', 'OG Title'), fieldTextarea('og_description', 'OG Description'), fieldImage('og_image_path', 'OG Image')] },
      { title: 'Canonical', columns: 2, fields: [fieldText('canonical_url', 'Canonical URL')] },
    ],
  },
  offers: {
    groups: [
      {
        title: 'Offers',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'offers',
            'Offers',
            'Offer',
            [
              fieldText('label', 'Label', 'SPECIAL'),
              fieldText('title', 'Title', 'New Offer'),
              fieldText('subtitle', 'Subtitle'),
              fieldText('cta_text', 'CTA Text', 'ORDER NOW'),
              fieldText('cta_link', 'CTA Link', '/menu'),
              fieldImage('image_path', 'Image'),
              fieldImage('bg_image_path', 'Background Image'),
              fieldText('style', 'Style'),
            ],
            () => ({
              label: null,
              title: 'New Offer',
              subtitle: null,
              cta_text: 'ORDER NOW',
              cta_link: '/menu',
              image_path: null,
              bg_image_path: null,
              style: null,
            }),
          ),
        ],
      },
    ],
  },
  'popular-dishes': {
    groups: [
      { title: 'Heading', columns: 2, fields: [fieldText('section_subtitle', 'Subtitle'), fieldText('section_title', 'Title')] },
      {
        title: 'Dishes',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'dishes',
            'Dishes',
            'Dish',
            [fieldText('name', 'Name', 'New Dish'), fieldTextarea('description', 'Description'), fieldText('price', 'Price', '$0'), fieldText('link', 'Link'), fieldImage('image_path', 'Image')],
            () => ({ name: 'New Dish', description: null, price: '0', image_path: null, link: null }),
          ),
        ],
      },
      { title: 'CTA', columns: 2, fields: [fieldText('cta_text', 'CTA Text', 'VIEW ALL ITEM'), fieldText('cta_link', 'CTA Link', '/menu')] },
    ],
  },
  cta: {
    groups: [
      { title: 'Text', columns: 2, fields: [fieldText('label', 'Label'), fieldText('title', 'Title'), fieldText('subtitle', 'Subtitle')] },
      { title: 'CTA', columns: 2, fields: [fieldText('cta_text', 'CTA Text', 'ORDER NOW'), fieldText('cta_link', 'CTA Link', '/menu')] },
      { title: 'Images', columns: 1, fields: [fieldImage('image_path', 'Image'), fieldImage('background_image_path', 'Background Image')] },
    ],
  },
  'food-menu': {
    groups: [
      { title: 'Heading', columns: 2, fields: [fieldText('section_subtitle', 'Subtitle'), fieldText('section_title', 'Title')] },
      {
        title: 'Categories',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'categories',
            'Categories',
            'Category',
            [
              fieldText('id', 'Category ID', 'fast-food'),
              fieldText('name', 'Category Name', 'Fast Food'),
              fieldImage('icon_path', 'Icon'),
              fieldArrayObjects(
                'items',
                'Menu Items',
                'Item',
                [fieldText('name', 'Name', 'New Menu Item'), fieldTextarea('description', 'Description'), fieldText('price', 'Price', '$0'), fieldImage('image_path', 'Image')],
                () => ({ name: 'New Menu Item', description: null, price: '0', image_path: null }),
              ),
            ],
            () => ({ id: `category-${Date.now()}`, name: 'New Category', icon_path: null, items: [] }),
          ),
        ],
      },
    ],
  },
  'special-offer': {
    groups: [
      { title: 'Heading', columns: 2, fields: [fieldText('section_subtitle', 'Subtitle'), fieldText('section_title', 'Title')] },
      { title: 'Countdown', columns: 2, fields: [fieldText('countdown_target', 'Countdown Target (ISO)', '2026-12-31T23:59:59Z')] },
      { title: 'CTA', columns: 2, fields: [fieldText('cta_text', 'CTA Text', 'ORDER NOW'), fieldText('cta_link', 'CTA Link', '/menu')] },
      { title: 'Images', columns: 1, fields: [fieldImage('image_path', 'Image'), fieldImage('background_image_path', 'Background Image')] },
    ],
  },
  chef: {
    groups: [
      { title: 'Heading', columns: 2, fields: [fieldText('section_subtitle', 'Subtitle'), fieldText('section_title', 'Title')] },
      {
        title: 'Team Members',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'members',
            'Members',
            'Member',
            [fieldText('name', 'Name', 'Chef'), fieldText('role', 'Role', 'Chef'), fieldImage('image_path', 'Image'), fieldKeyValue('social_links', 'Social Links', { presets: SOCIAL_PRESETS })],
            () => ({ name: 'Chef', role: null, image_path: null, social_links: {} }),
          ),
        ],
      },
    ],
  },
  'client-logos': {
    groups: [
      {
        title: 'Client Logos',
        columns: 1,
        fields: [
          fieldArrayObjects(
            'logos',
            'Logos',
            'Logo',
            [fieldImage('image_path', 'Logo Image'), fieldText('alt_text', 'Alt Text'), fieldText('link', 'Link')],
            () => ({ image_path: '', alt_text: null, link: null }),
          ),
        ],
      },
    ],
  },
};

function apiUrl(path) {
  return `${API_BASE}${path}`;
}

function setToken(username, password) {
  const token = btoa(`${username}:${password}`);
  state.token = token;
  localStorage.setItem('adminToken', token);
}

function clearToken() {
  state.token = '';
  localStorage.removeItem('adminToken');
}

function notify(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add('show');
  window.clearTimeout(elements.toast._timer);
  elements.toast._timer = window.setTimeout(() => {
    elements.toast.classList.remove('show');
  }, 2800);
}

function addActivity(message) {
  const entry = { message, timestamp: new Date().toLocaleString() };
  state.activity.unshift(entry);
  if (state.activity.length > 8) {
    state.activity.pop();
  }
  renderActivity();
}

function renderActivity() {
  elements.activityFeed.innerHTML = '';
  if (state.activity.length === 0) {
    elements.activityFeed.innerHTML = '<div class="timeline-item">Ready when you are.</div>';
    return;
  }
  state.activity.forEach((item) => {
    const div = document.createElement('div');
    div.className = 'timeline-item';
    div.textContent = `${item.timestamp} - ${item.message}`;
    elements.activityFeed.appendChild(div);
  });
}

async function apiRequest(path, options = {}, auth = true) {
  const headers = new Headers(options.headers || {});
  if (auth && state.token) {
    headers.set('Authorization', `Basic ${state.token}`);
  }
  const config = { ...options, headers };
  const response = await fetch(apiUrl(path), config);
  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json') ? await response.json() : null;

  if (!response.ok || (payload && payload.success === false)) {
    const message = payload && payload.message ? payload.message : response.statusText;
    throw new Error(message || 'Request failed');
  }
  return payload;
}

async function checkSession() {
  if (!state.token) {
    return false;
  }
  try {
    const payload = await apiRequest('/api/v1/auth/me');
    state.user = payload.data.username;
    return true;
  } catch (error) {
    clearToken();
    return false;
  }
}

function showApp() {
  elements.loginView.style.display = 'none';
  elements.appView.style.display = 'grid';
  elements.appView.setAttribute('aria-hidden', 'false');
  elements.currentUser.textContent = state.user ? `Signed in as ${state.user}` : 'Signed in';
  elements.apiBase.textContent = API_BASE || '/';
}

function showLogin() {
  elements.loginView.style.display = 'grid';
  elements.appView.style.display = 'none';
  elements.appView.setAttribute('aria-hidden', 'true');
}

function setView(viewId, title, subtitle) {
  document.querySelectorAll('.view').forEach((view) => {
    view.classList.remove('active');
  });
  document.getElementById(viewId).classList.add('active');
  elements.viewTitle.textContent = title;
  elements.viewSubtitle.textContent = subtitle;
  document.querySelectorAll('.nav-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.view === viewId.replace('View', ''));
  });
}

async function loadDashboard() {
  try {
    const health = await apiRequest('/api/v1/health', {}, false);
    const status = health.data.status;
    elements.healthStatus.textContent = status.toUpperCase();
    elements.healthMeta.textContent = `DB: ${health.data.components.database.status}`;
    elements.envPill.textContent = health.data.environment;
    elements.envValue.textContent = health.data.environment;
  } catch (error) {
    elements.healthStatus.textContent = 'ERROR';
    elements.healthMeta.textContent = error.message;
  }

  try {
    const news = await apiRequest(`/api/v1/news/admin/list?page=1&page_size=1`);
    elements.newsCount.textContent = news.data.total;
  } catch (error) {
    elements.newsCount.textContent = '-';
  }

  try {
    const assets = await apiRequest(`/api/v1/assets?page=1&page_size=1`);
    elements.assetCount.textContent = assets.data.total;
  } catch (error) {
    elements.assetCount.textContent = '-';
  }
}

function renderCmsList() {
  elements.cmsSectionList.innerHTML = '';
  cmsSections.forEach((section) => {
    const button = document.createElement('button');
    button.textContent = section.name;
    button.className = section.id === state.cms.current ? 'active' : '';
    button.addEventListener('click', () => selectCmsSection(section.id));
    elements.cmsSectionList.appendChild(button);
  });
}

function selectCmsSection(sectionId) {
  state.cms.current = sectionId;
  const section = cmsSections.find((item) => item.id === sectionId);
  if (!section) {
    return;
  }

  elements.cmsSectionTitle.textContent = section.name;
  elements.cmsSectionHint.textContent = section.readonly ? 'Read-only preview' : 'Edit fields and save';
  elements.cmsSaveBtn.disabled = Boolean(section.readonly);
  if (elements.cmsEditor) {
    elements.cmsEditor.readOnly = true;
  }
  renderCmsList();
  loadCmsSection();
}

function sanitizeCmsPayload(payload) {
  if (!payload || typeof payload !== 'object') {
    return payload;
  }
  const cleaned = { ...payload };
  delete cleaned.id;
  delete cleaned.created_at;
  delete cleaned.updated_at;
  return cleaned;
}

function cloneJson(value) {
  if (value === null || value === undefined) {
    return value;
  }
  return JSON.parse(JSON.stringify(value));
}

function joinPath(prefix, key) {
  if (!prefix) {
    return key;
  }
  return `${prefix}.${key}`;
}

function pathToSegments(path) {
  const segments = [];
  const re = /[^.[\]]+|\[(\d+)\]/g;
  let match;
  while ((match = re.exec(path)) !== null) {
    if (match[1] !== undefined) {
      segments.push(Number(match[1]));
    } else {
      segments.push(match[0]);
    }
  }
  return segments;
}

function getValueAtPath(obj, path) {
  if (!path) {
    return obj;
  }
  const segments = pathToSegments(path);
  let cursor = obj;
  for (const segment of segments) {
    if (cursor === null || cursor === undefined) {
      return undefined;
    }
    cursor = cursor[segment];
  }
  return cursor;
}

function setValueAtPath(obj, path, value) {
  const segments = pathToSegments(path);
  if (segments.length === 0) {
    return;
  }
  let cursor = obj;
  for (let i = 0; i < segments.length - 1; i += 1) {
    const segment = segments[i];
    const next = segments[i + 1];
    if (cursor[segment] === undefined || cursor[segment] === null) {
      cursor[segment] = typeof next === 'number' ? [] : {};
    }
    cursor = cursor[segment];
  }
  cursor[segments[segments.length - 1]] = value;
}

function ensureArrayAtPath(path) {
  const current = getValueAtPath(state.cms.draft, path);
  if (Array.isArray(current)) {
    return current;
  }
  const fresh = [];
  setValueAtPath(state.cms.draft, path, fresh);
  return fresh;
}

function ensureObjectAtPath(path) {
  const current = getValueAtPath(state.cms.draft, path);
  if (current && typeof current === 'object' && !Array.isArray(current)) {
    return current;
  }
  const fresh = {};
  setValueAtPath(state.cms.draft, path, fresh);
  return fresh;
}

function resolvedCmsUrl(value) {
  if (!value) {
    return '';
  }
  if (typeof value !== 'string') {
    return '';
  }
  if (value.startsWith('http://') || value.startsWith('https://')) {
    return value;
  }
  if (value.startsWith('/')) {
    return `${API_BASE}${value}`;
  }
  return `${API_BASE}/${value}`;
}

const scheduleCmsPreviewUpdate = (() => {
  let timer = null;
  return () => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => {
      if (!elements.cmsEditor) {
        return;
      }
      elements.cmsEditor.value = JSON.stringify(state.cms.draft || {}, null, 2);
    }, 120);
  };
})();

function openAssetPicker(onSelect) {
  state.assetPicker.open = true;
  state.assetPicker.onSelect = onSelect;
  state.assetPicker.page = 1;
  state.assetPicker.search = '';
  state.assetPicker.items = [];
  if (elements.assetPickerSearch) {
    elements.assetPickerSearch.value = '';
  }
  elements.assetPicker.classList.add('show');
  elements.assetPicker.setAttribute('aria-hidden', 'false');
  loadAssetPicker();
}

function closeAssetPicker() {
  state.assetPicker.open = false;
  state.assetPicker.onSelect = null;
  elements.assetPicker.classList.remove('show');
  elements.assetPicker.setAttribute('aria-hidden', 'true');
}

async function loadAssetPicker() {
  try {
    const payload = await apiRequest(
      `/api/v1/assets?page=${state.assetPicker.page}&page_size=${state.assetPicker.pageSize}`,
    );
    const total = payload.data.total || 0;
    state.assetPicker.totalPages = Math.max(1, Math.ceil(total / state.assetPicker.pageSize));
    state.assetPicker.items = payload.data.items || [];
    renderAssetPicker();
  } catch (error) {
    notify(`Failed to load assets: ${error.message}`);
  }
}

function renderAssetPicker() {
  const search = (state.assetPicker.search || '').toLowerCase();
  const items = state.assetPicker.items || [];
  const filtered = search
    ? items.filter((asset) => {
        const name = `${asset.original_filename || ''} ${asset.filename || ''}`.toLowerCase();
        return name.includes(search);
      })
    : items;

  elements.assetPickerGrid.innerHTML = '';
  filtered.forEach((asset) => {
    const card = document.createElement('div');
    card.className = 'asset-card asset-picker-card';

    const img = document.createElement('img');
    img.className = 'asset-thumb';
    img.src = resolvedFileUrl(asset);
    img.alt = asset.alt_text || asset.filename;
    card.appendChild(img);

    const title = document.createElement('div');
    title.textContent = asset.original_filename || asset.filename;
    card.appendChild(title);

    const meta = document.createElement('div');
    meta.className = 'asset-meta';
    meta.textContent = `Category: ${asset.category || 'none'}`;
    card.appendChild(meta);

    card.addEventListener('click', () => {
      if (typeof state.assetPicker.onSelect === 'function') {
        state.assetPicker.onSelect(asset);
      }
      closeAssetPicker();
    });

    elements.assetPickerGrid.appendChild(card);
  });

  buildPagination(elements.assetPickerPagination, state.assetPicker.page, state.assetPicker.totalPages, (page) => {
    state.assetPicker.page = page;
    loadAssetPicker();
  });
}

function renderInputField(def, path) {
  const label = document.createElement('label');
  label.textContent = def.label;

  const input = document.createElement('input');
  input.type = def.type === 'number' ? 'number' : 'text';
  if (def.placeholder) {
    input.placeholder = def.placeholder;
  }
  if (def.type === 'number') {
    if (def.min !== undefined) input.min = String(def.min);
    if (def.max !== undefined) input.max = String(def.max);
    if (def.step !== undefined) input.step = String(def.step);
  }

  const currentValue = getValueAtPath(state.cms.draft, path);
  input.value = currentValue === null || currentValue === undefined ? '' : String(currentValue);

  input.addEventListener('input', () => {
    if (def.type === 'number') {
      const parsed = input.value === '' ? null : Number(input.value);
      setValueAtPath(state.cms.draft, path, Number.isNaN(parsed) ? null : parsed);
    } else {
      setValueAtPath(state.cms.draft, path, input.value);
    }
    scheduleCmsPreviewUpdate();
  });

  label.appendChild(input);
  if (def.full) {
    label.classList.add('full');
  }
  return label;
}

function renderTextareaField(def, path) {
  const label = document.createElement('label');
  label.textContent = def.label;

  const textarea = document.createElement('textarea');
  if (def.placeholder) {
    textarea.placeholder = def.placeholder;
  }
  const currentValue = getValueAtPath(state.cms.draft, path);
  textarea.value = currentValue === null || currentValue === undefined ? '' : String(currentValue);

  textarea.addEventListener('input', () => {
    setValueAtPath(state.cms.draft, path, textarea.value);
    scheduleCmsPreviewUpdate();
  });

  label.appendChild(textarea);
  label.classList.add('full');
  return label;
}

function renderBooleanField(def, path) {
  const wrap = document.createElement('div');
  wrap.className = 'check-row full';

  const label = document.createElement('label');
  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.checked = Boolean(getValueAtPath(state.cms.draft, path));
  checkbox.addEventListener('change', () => {
    setValueAtPath(state.cms.draft, path, checkbox.checked);
    scheduleCmsPreviewUpdate();
  });

  const text = document.createElement('span');
  text.textContent = def.label;
  label.appendChild(checkbox);
  label.appendChild(text);
  wrap.appendChild(label);
  return wrap;
}

async function uploadImageFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  const payload = await apiRequest('/api/v1/assets/upload', { method: 'POST', body: formData });
  return payload.data;
}

function renderImageField(def, path, labelOverride = null) {
  const container = document.createElement('div');
  container.className = 'image-field';
  if (def.full) {
    container.classList.add('full');
  }

  const label = document.createElement('label');
  label.textContent = labelOverride || def.label;

  const input = document.createElement('input');
  input.type = 'text';
  input.placeholder = '/static/uploads/...';
  const currentValue = getValueAtPath(state.cms.draft, path);
  input.value = currentValue === null || currentValue === undefined ? '' : String(currentValue);
  label.appendChild(input);
  container.appendChild(label);

  const preview = document.createElement('img');
  preview.className = 'image-preview';
  const previewUrl = resolvedCmsUrl(input.value);
  if (previewUrl) {
    preview.src = previewUrl;
    preview.style.display = 'block';
  } else {
    preview.style.display = 'none';
  }
  container.appendChild(preview);

  const actions = document.createElement('div');
  actions.className = 'field-actions';

  const uploadBtn = document.createElement('button');
  uploadBtn.type = 'button';
  uploadBtn.className = 'btn ghost small';
  uploadBtn.textContent = 'Upload';

  const pickBtn = document.createElement('button');
  pickBtn.type = 'button';
  pickBtn.className = 'btn ghost small';
  pickBtn.textContent = 'Pick';

  const clearBtn = document.createElement('button');
  clearBtn.type = 'button';
  clearBtn.className = 'btn ghost small';
  clearBtn.textContent = 'Clear';

  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = 'image/*';
  fileInput.style.display = 'none';

  uploadBtn.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', async () => {
    if (!fileInput.files || !fileInput.files[0]) {
      return;
    }
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';
    try {
      const asset = await uploadImageFile(fileInput.files[0]);
      const url = asset.file_url || asset.file_path || '';
      setValueAtPath(state.cms.draft, path, url);
      input.value = url;
      const nextUrl = resolvedCmsUrl(url);
      if (nextUrl) {
        preview.src = nextUrl;
        preview.style.display = 'block';
      }
      notify('Uploaded image');
      addActivity('Uploaded image');
      scheduleCmsPreviewUpdate();
    } catch (error) {
      notify(`Upload failed: ${error.message}`);
    } finally {
      uploadBtn.disabled = false;
      uploadBtn.textContent = 'Upload';
      fileInput.value = '';
    }
  });

  pickBtn.addEventListener('click', () => {
    openAssetPicker((asset) => {
      const url = asset.file_url || '';
      setValueAtPath(state.cms.draft, path, url);
      input.value = url;
      const nextUrl = resolvedCmsUrl(url);
      if (nextUrl) {
        preview.src = nextUrl;
        preview.style.display = 'block';
      }
      scheduleCmsPreviewUpdate();
    });
  });

  clearBtn.addEventListener('click', () => {
    setValueAtPath(state.cms.draft, path, null);
    input.value = '';
    preview.style.display = 'none';
    scheduleCmsPreviewUpdate();
  });

  input.addEventListener('input', () => {
    const value = input.value.trim();
    setValueAtPath(state.cms.draft, path, value || null);
    const nextUrl = resolvedCmsUrl(value);
    if (nextUrl) {
      preview.src = nextUrl;
      preview.style.display = 'block';
    } else {
      preview.style.display = 'none';
    }
    scheduleCmsPreviewUpdate();
  });

  actions.appendChild(uploadBtn);
  actions.appendChild(pickBtn);
  actions.appendChild(clearBtn);
  container.appendChild(actions);
  container.appendChild(fileInput);
  return container;
}

function renderKeyValueField(def, path) {
  const container = document.createElement('div');
  container.className = 'repeater full';

  const header = document.createElement('div');
  header.className = 'repeater-header';
  const title = document.createElement('div');
  title.className = 'repeater-item-title';
  title.textContent = def.label;
  header.appendChild(title);
  container.appendChild(header);

  const presets = def.presets || [];
  const current = getValueAtPath(state.cms.draft, path);
  const values = current && typeof current === 'object' && !Array.isArray(current) ? current : {};
  const customKeys = Object.keys(values).filter((k) => !presets.includes(k));

  if (presets.length) {
    const grid = document.createElement('div');
    grid.className = 'form-grid two';
    presets.forEach((key) => {
      const label = document.createElement('label');
      label.textContent = key;
      const input = document.createElement('input');
      input.type = 'text';
      input.placeholder = `https://${key}.com/...`;
      input.value = values[key] || '';
      input.addEventListener('input', () => {
        const obj = ensureObjectAtPath(path);
        const v = input.value.trim();
        if (!v) {
          delete obj[key];
        } else {
          obj[key] = v;
        }
        if (Object.keys(obj).length === 0) {
          setValueAtPath(state.cms.draft, path, null);
        }
        scheduleCmsPreviewUpdate();
      });
      label.appendChild(input);
      grid.appendChild(label);
    });
    container.appendChild(grid);
  }

  if (customKeys.length) {
    const customWrap = document.createElement('div');
    customWrap.className = 'repeater';
    customKeys.forEach((key) => {
      const item = document.createElement('div');
      item.className = 'repeater-item';

      const rowHeader = document.createElement('div');
      rowHeader.className = 'repeater-header';
      const k = document.createElement('div');
      k.className = 'repeater-item-title';
      k.textContent = key;
      rowHeader.appendChild(k);

      const removeBtn = document.createElement('button');
      removeBtn.type = 'button';
      removeBtn.className = 'btn ghost small';
      removeBtn.textContent = 'Remove';
      removeBtn.addEventListener('click', () => {
        const obj = ensureObjectAtPath(path);
        delete obj[key];
        if (Object.keys(obj).length === 0) {
          setValueAtPath(state.cms.draft, path, null);
        }
        renderCmsForm();
        scheduleCmsPreviewUpdate();
      });
      rowHeader.appendChild(removeBtn);
      item.appendChild(rowHeader);

      const valueLabel = document.createElement('label');
      valueLabel.textContent = 'URL';
      const input = document.createElement('input');
      input.type = 'text';
      input.value = values[key] || '';
      input.addEventListener('input', () => {
        const obj = ensureObjectAtPath(path);
        const v = input.value.trim();
        if (!v) {
          delete obj[key];
        } else {
          obj[key] = v;
        }
        scheduleCmsPreviewUpdate();
      });
      valueLabel.appendChild(input);
      item.appendChild(valueLabel);

      customWrap.appendChild(item);
    });
    container.appendChild(customWrap);
  }

  const addWrap = document.createElement('div');
  addWrap.className = 'repeater-item';
  const addHeader = document.createElement('div');
  addHeader.className = 'repeater-header';
  const addTitle = document.createElement('div');
  addTitle.className = 'repeater-item-title';
  addTitle.textContent = 'Add custom link';
  addHeader.appendChild(addTitle);
  addWrap.appendChild(addHeader);

  const addGrid = document.createElement('div');
  addGrid.className = 'form-grid two';
  const keyLabel = document.createElement('label');
  keyLabel.textContent = 'Key';
  const keyInput = document.createElement('input');
  keyInput.type = 'text';
  keyInput.placeholder = 'custom_name';
  keyLabel.appendChild(keyInput);
  addGrid.appendChild(keyLabel);

  const valLabel = document.createElement('label');
  valLabel.textContent = 'URL';
  const valInput = document.createElement('input');
  valInput.type = 'text';
  valInput.placeholder = 'https://...';
  valLabel.appendChild(valInput);
  addGrid.appendChild(valLabel);

  const addBtn = document.createElement('button');
  addBtn.type = 'button';
  addBtn.className = 'btn ghost small';
  addBtn.textContent = 'Add';
  addBtn.addEventListener('click', () => {
    const key = keyInput.value.trim();
    if (!key) {
      notify('Enter a key');
      return;
    }
    const obj = ensureObjectAtPath(path);
    obj[key] = valInput.value.trim();
    keyInput.value = '';
    valInput.value = '';
    renderCmsForm();
    scheduleCmsPreviewUpdate();
  });

  const actions = document.createElement('div');
  actions.className = 'field-actions';
  actions.appendChild(addBtn);

  addWrap.appendChild(addGrid);
  addWrap.appendChild(actions);
  container.appendChild(addWrap);
  return container;
}

function splitArrayItemPath(path) {
  const match = path.match(/^(.*)\[(\d+)\]$/);
  if (!match) {
    return null;
  }
  return { parentPath: match[1], index: Number(match[2]) };
}

function defaultNavItem() {
  return { label: 'New Item', link: '/', has_dropdown: false, children: [] };
}

function renderNavField(def, path) {
  const container = document.createElement('div');
  container.className = 'repeater full';

  const header = document.createElement('div');
  header.className = 'repeater-header';
  const title = document.createElement('div');
  title.className = 'repeater-item-title';
  title.textContent = def.label;
  header.appendChild(title);

  const addBtn = document.createElement('button');
  addBtn.type = 'button';
  addBtn.className = 'btn ghost small';
  addBtn.textContent = 'Add item';
  addBtn.addEventListener('click', () => {
    const items = ensureArrayAtPath(path);
    items.push(defaultNavItem());
    renderCmsForm();
    scheduleCmsPreviewUpdate();
  });
  header.appendChild(addBtn);
  container.appendChild(header);

  const tree = document.createElement('div');
  tree.className = 'nav-tree';

  const items = getValueAtPath(state.cms.draft, path);
  const list = Array.isArray(items) ? items : [];
  list.forEach((_, idx) => {
    tree.appendChild(renderNavNode(`${path}[${idx}]`));
  });
  container.appendChild(tree);
  return container;
}

function renderNavNode(itemPath) {
  const node = document.createElement('div');
  node.className = 'nav-node';
  const item = getValueAtPath(state.cms.draft, itemPath) || {};

  const grid = document.createElement('div');
  grid.className = 'form-grid two';
  grid.appendChild(renderInputField({ type: 'text', label: 'Label' }, joinPath(itemPath, 'label')));
  grid.appendChild(renderInputField({ type: 'text', label: 'Link', placeholder: '/' }, joinPath(itemPath, 'link')));
  node.appendChild(grid);

  const check = renderBooleanField({ label: 'Has dropdown' }, joinPath(itemPath, 'has_dropdown'));
  check.classList.remove('full');
  node.appendChild(check);

  const actions = document.createElement('div');
  actions.className = 'field-actions';

  const addChildBtn = document.createElement('button');
  addChildBtn.type = 'button';
  addChildBtn.className = 'btn ghost small';
  addChildBtn.textContent = 'Add child';
  addChildBtn.addEventListener('click', () => {
    const childrenPath = joinPath(itemPath, 'children');
    const children = ensureArrayAtPath(childrenPath);
    children.push(defaultNavItem());
    renderCmsForm();
    scheduleCmsPreviewUpdate();
  });

  const removeBtn = document.createElement('button');
  removeBtn.type = 'button';
  removeBtn.className = 'btn ghost small';
  removeBtn.textContent = 'Remove';
  removeBtn.addEventListener('click', () => {
    const info = splitArrayItemPath(itemPath);
    if (!info) {
      return;
    }
    const list = ensureArrayAtPath(info.parentPath);
    list.splice(info.index, 1);
    renderCmsForm();
    scheduleCmsPreviewUpdate();
  });

  actions.appendChild(addChildBtn);
  actions.appendChild(removeBtn);
  node.appendChild(actions);

  const children = item.children;
  if (Array.isArray(children) && children.length > 0) {
    const childWrap = document.createElement('div');
    childWrap.className = 'nav-children';
    children.forEach((_, idx) => {
      childWrap.appendChild(renderNavNode(`${itemPath}.children[${idx}]`));
    });
    node.appendChild(childWrap);
  }

  return node;
}

function renderArrayField(def, path) {
  const container = document.createElement('div');
  container.className = 'repeater full';

  const header = document.createElement('div');
  header.className = 'repeater-header';
  const title = document.createElement('div');
  title.className = 'repeater-item-title';
  title.textContent = def.label;
  header.appendChild(title);

  const addBtn = document.createElement('button');
  addBtn.type = 'button';
  addBtn.className = 'btn ghost small';
  addBtn.textContent = `Add ${def.itemLabel || 'item'}`;
  addBtn.addEventListener('click', () => {
    const list = ensureArrayAtPath(path);
    const next = typeof def.defaultItem === 'function' ? def.defaultItem() : def.defaultItem;
    list.push(next);
    renderCmsForm();
    scheduleCmsPreviewUpdate();
  });
  header.appendChild(addBtn);
  container.appendChild(header);

  const listValue = getValueAtPath(state.cms.draft, path);
  const list = Array.isArray(listValue) ? listValue : [];

  list.forEach((_, idx) => {
    const itemPath = `${path}[${idx}]`;
    const item = document.createElement('div');
    item.className = 'repeater-item';

    const itemHeader = document.createElement('div');
    itemHeader.className = 'repeater-header';
    const itemTitle = document.createElement('div');
    itemTitle.className = 'repeater-item-title';
    itemTitle.textContent = `${def.itemLabel || 'Item'} #${idx + 1}`;
    itemHeader.appendChild(itemTitle);

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'btn ghost small';
    removeBtn.textContent = 'Remove';
    removeBtn.addEventListener('click', () => {
      const list = ensureArrayAtPath(path);
      list.splice(idx, 1);
      renderCmsForm();
      scheduleCmsPreviewUpdate();
    });
    itemHeader.appendChild(removeBtn);
    item.appendChild(itemHeader);

    if (def.itemFields) {
      const grid = document.createElement('div');
      grid.className = 'form-grid two';
      def.itemFields.forEach((field) => {
        const el = renderField(field, itemPath);
        if (field.full) {
          el.classList.add('full');
        }
        grid.appendChild(el);
      });
      item.appendChild(grid);
    } else if (def.item) {
      if (def.item.type === 'image') {
        item.appendChild(renderImageField(def.item, itemPath, def.item.label || 'Image'));
      } else if (def.item.type === 'text') {
        item.appendChild(renderInputField({ type: 'text', label: def.item.label || 'Value', placeholder: def.item.placeholder || '' }, itemPath));
      } else {
        item.appendChild(renderInputField({ type: 'text', label: def.item.label || 'Value' }, itemPath));
      }
    }

    container.appendChild(item);
  });

  return container;
}

function renderField(def, basePath) {
  const path = def.key ? joinPath(basePath, def.key) : basePath;
  if (def.type === 'textarea') {
    return renderTextareaField(def, path);
  }
  if (def.type === 'boolean') {
    return renderBooleanField(def, path);
  }
  if (def.type === 'image') {
    return renderImageField(def, path);
  }
  if (def.type === 'array') {
    return renderArrayField(def, path);
  }
  if (def.type === 'keyvalue') {
    return renderKeyValueField(def, path);
  }
  if (def.type === 'nav') {
    return renderNavField(def, path);
  }
  return renderInputField(def, path);
}

function renderCmsForm() {
  const section = cmsSections.find((item) => item.id === state.cms.current);
  if (!section) {
    return;
  }

  elements.cmsForm.innerHTML = '';

  if (!state.cms.draft) {
    const div = document.createElement('div');
    div.className = 'subtle';
    div.textContent = 'Load a section to start editing.';
    elements.cmsForm.appendChild(div);
    return;
  }

  if (section.readonly || section.id === 'home') {
    const panel = document.createElement('div');
    panel.className = 'form-section';
    const title = document.createElement('h4');
    title.textContent = 'Read-only preview';
    const text = document.createElement('div');
    text.className = 'subtle';
    text.textContent = 'Select a section on the left to edit content. This view is a combined preview.';
    panel.appendChild(title);
    panel.appendChild(text);
    elements.cmsForm.appendChild(panel);
    if (elements.cmsAdvanced) {
      elements.cmsAdvanced.open = true;
    }
    scheduleCmsPreviewUpdate();
    return;
  }

  const config = cmsFormConfigs[section.id];
  if (!config) {
    const panel = document.createElement('div');
    panel.className = 'form-section';
    const title = document.createElement('h4');
    title.textContent = 'No form available';
    const text = document.createElement('div');
    text.className = 'subtle';
    text.textContent = 'This section is not configured yet. Use the Advanced JSON preview.';
    panel.appendChild(title);
    panel.appendChild(text);
    elements.cmsForm.appendChild(panel);
    scheduleCmsPreviewUpdate();
    return;
  }

  config.groups.forEach((group) => {
    const groupEl = document.createElement('div');
    groupEl.className = 'form-section';
    const h = document.createElement('h4');
    h.textContent = group.title;
    groupEl.appendChild(h);

    const grid = document.createElement('div');
    grid.className = group.columns === 1 ? 'form-grid' : 'form-grid two';

    group.fields.forEach((field) => {
      const el = renderField(field, '');
      if (field.full) {
        el.classList.add('full');
      }
      grid.appendChild(el);
    });

    groupEl.appendChild(grid);
    elements.cmsForm.appendChild(groupEl);
  });

  scheduleCmsPreviewUpdate();
}

async function loadCmsSection() {
  const section = cmsSections.find((item) => item.id === state.cms.current);
  if (!section) {
    return;
  }
  try {
    elements.cmsForm.innerHTML = '<div class="subtle">Loading...</div>';
    const payload = await apiRequest(section.endpoint);
    state.cms.data = payload.data;
    state.cms.draft = sanitizeCmsPayload(cloneJson(payload.data)) || {};
    if (elements.cmsEditor) {
      elements.cmsEditor.value = JSON.stringify(state.cms.draft, null, 2);
    }
    renderCmsForm();
    notify(`Loaded ${section.name}`);
  } catch (error) {
    notify(`Failed to load: ${error.message}`);
  }
}

async function saveCmsSection() {
  const section = cmsSections.find((item) => item.id === state.cms.current);
  if (!section || section.readonly) {
    return;
  }
  try {
    const cleaned = sanitizeCmsPayload(cloneJson(state.cms.draft || {}));
    await apiRequest(section.endpoint, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cleaned),
    });
    notify(`${section.name} updated`);
    addActivity(`Updated ${section.name}`);
    await loadCmsSection();
  } catch (error) {
    notify(`Save failed: ${error.message}`);
  }
}

function buildPagination(container, current, totalPages, onSelect) {
  container.innerHTML = '';
  if (totalPages <= 1) {
    return;
  }
  const pages = [];
  const start = Math.max(1, current - 2);
  const end = Math.min(totalPages, current + 2);
  for (let i = start; i <= end; i += 1) {
    pages.push(i);
  }
  pages.forEach((page) => {
    const btn = document.createElement('button');
    btn.className = `page-btn${page === current ? ' active' : ''}`;
    btn.textContent = page;
    btn.addEventListener('click', () => onSelect(page));
    container.appendChild(btn);
  });
}

function formatStatus(isPublished) {
  const span = document.createElement('span');
  span.className = `status-pill ${isPublished ? 'published' : 'draft'}`;
  span.textContent = isPublished ? 'Published' : 'Draft';
  return span;
}

function toLocalDateTime(value) {
  if (!value) {
    return '';
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return '';
  }
  return date.toISOString().slice(0, 16);
}

async function loadNewsList() {
  const category = elements.newsCategoryFilter.value.trim();
  const status = elements.newsStatusFilter.value;
  const params = new URLSearchParams({
    page: state.news.page.toString(),
    page_size: state.news.pageSize.toString(),
  });
  if (category) {
    params.set('category', category);
  }
  if (status) {
    params.set('is_published', status);
  }

  try {
    const payload = await apiRequest(`/api/v1/news/admin/list?${params.toString()}`);
    state.news.total = payload.data.total;
    renderNewsTable(payload.data.items || []);
    buildPagination(elements.newsPagination, payload.data.page, payload.data.total_pages, (page) => {
      state.news.page = page;
      loadNewsList();
    });
  } catch (error) {
    notify(`Failed to load news: ${error.message}`);
  }
}

function renderNewsTable(items) {
  elements.newsTableBody.innerHTML = '';
  items.forEach((item) => {
    const row = document.createElement('tr');
    const titleCell = document.createElement('td');
    titleCell.textContent = item.title;
    const categoryCell = document.createElement('td');
    categoryCell.textContent = item.category || '-';
    const statusCell = document.createElement('td');
    statusCell.appendChild(formatStatus(item.is_published));
    const dateCell = document.createElement('td');
    dateCell.textContent = item.published_at ? new Date(item.published_at).toLocaleDateString() : '-';
    const actionCell = document.createElement('td');
    const actionWrap = document.createElement('div');
    actionWrap.className = 'table-actions';

    const editBtn = document.createElement('button');
    editBtn.className = 'btn ghost';
    editBtn.textContent = 'Edit';
    editBtn.addEventListener('click', () => loadNewsIntoForm(item));

    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'btn ghost';
    toggleBtn.textContent = item.is_published ? 'Unpublish' : 'Publish';
    toggleBtn.addEventListener('click', () => togglePublish(item));

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn ghost';
    deleteBtn.textContent = 'Delete';
    deleteBtn.addEventListener('click', () => deleteNews(item.id));

    actionWrap.appendChild(editBtn);
    actionWrap.appendChild(toggleBtn);
    actionWrap.appendChild(deleteBtn);
    actionCell.appendChild(actionWrap);

    row.appendChild(titleCell);
    row.appendChild(categoryCell);
    row.appendChild(statusCell);
    row.appendChild(dateCell);
    row.appendChild(actionCell);
    elements.newsTableBody.appendChild(row);
  });
}

function loadNewsIntoForm(item) {
  elements.newsFormTitle.textContent = `Edit: ${item.title}`;
  elements.newsId.value = item.id;
  elements.newsTitle.value = item.title || '';
  elements.newsSlug.value = item.slug || '';
  elements.newsCategory.value = item.category || '';
  elements.newsAuthor.value = item.author || '';
  elements.newsCover.value = item.cover_image_path || '';
  elements.newsTags.value = item.tags || '';
  elements.newsSummary.value = item.summary || '';
  elements.newsContent.value = item.content || '';
  elements.newsMetaTitle.value = item.meta_title || '';
  elements.newsMetaDescription.value = item.meta_description || '';
  elements.newsPublished.checked = Boolean(item.is_published);
  elements.newsPublishedAt.value = toLocalDateTime(item.published_at);
}

function resetNewsForm() {
  elements.newsFormTitle.textContent = 'Create Article';
  elements.newsForm.reset();
  elements.newsId.value = '';
}

async function saveNews(event) {
  event.preventDefault();
  const payload = {
    title: elements.newsTitle.value.trim(),
    slug: elements.newsSlug.value.trim() || null,
    summary: elements.newsSummary.value.trim() || null,
    content: elements.newsContent.value.trim() || null,
    cover_image_path: elements.newsCover.value.trim() || null,
    author: elements.newsAuthor.value.trim() || null,
    category: elements.newsCategory.value.trim() || null,
    tags: elements.newsTags.value.trim() || null,
    meta_title: elements.newsMetaTitle.value.trim() || null,
    meta_description: elements.newsMetaDescription.value.trim() || null,
    is_published: elements.newsPublished.checked,
  };
  const publishedAtValue = elements.newsPublishedAt.value;
  if (publishedAtValue) {
    payload.published_at = new Date(publishedAtValue).toISOString();
  }

  try {
    if (elements.newsId.value) {
      await apiRequest(`/api/v1/news/${elements.newsId.value}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      notify('Article updated');
      addActivity(`Updated article: ${payload.title}`);
    } else {
      await apiRequest('/api/v1/news', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      notify('Article created');
      addActivity(`Created article: ${payload.title}`);
    }
    resetNewsForm();
    loadNewsList();
  } catch (error) {
    notify(`Save failed: ${error.message}`);
  }
}

async function deleteNews(id) {
  if (!window.confirm('Delete this article?')) {
    return;
  }
  try {
    await apiRequest(`/api/v1/news/${id}`, { method: 'DELETE' });
    notify('Article deleted');
    addActivity(`Deleted article ${id}`);
    loadNewsList();
  } catch (error) {
    notify(`Delete failed: ${error.message}`);
  }
}

async function togglePublish(item) {
  try {
    if (item.is_published) {
      await apiRequest(`/api/v1/news/${item.id}/unpublish`, { method: 'PATCH' });
      notify('Article unpublished');
      addActivity(`Unpublished article: ${item.title}`);
    } else {
      await apiRequest(`/api/v1/news/${item.id}/publish`, { method: 'PATCH' });
      notify('Article published');
      addActivity(`Published article: ${item.title}`);
    }
    loadNewsList();
  } catch (error) {
    notify(`Publish action failed: ${error.message}`);
  }
}

async function uploadAsset(event) {
  event.preventDefault();
  if (!elements.assetFile.files[0]) {
    notify('Select a file to upload');
    return;
  }
  const formData = new FormData();
  formData.append('file', elements.assetFile.files[0]);
  if (elements.assetCategory.value.trim()) {
    formData.append('category', elements.assetCategory.value.trim());
  }
  if (elements.assetAltText.value.trim()) {
    formData.append('alt_text', elements.assetAltText.value.trim());
  }
  try {
    await apiRequest('/api/v1/assets/upload', { method: 'POST', body: formData });
    notify('Asset uploaded');
    addActivity('Uploaded new asset');
    elements.assetUploadForm.reset();
    loadAssets();
  } catch (error) {
    notify(`Upload failed: ${error.message}`);
  }
}

function resolvedFileUrl(asset) {
  if (asset.file_url) {
    return asset.file_url.startsWith('http') ? asset.file_url : `${API_BASE}${asset.file_url}`;
  }
  return `${API_BASE}/static/uploads/${asset.file_path}`;
}

async function loadAssets() {
  try {
    const payload = await apiRequest(`/api/v1/assets?page=${state.assets.page}&page_size=${state.assets.pageSize}`);
    state.assets.total = payload.data.total;
    renderAssets(payload.data.items || []);
    const totalPages = Math.max(1, Math.ceil(state.assets.total / state.assets.pageSize));
    buildPagination(elements.assetPagination, state.assets.page, totalPages, (page) => {
      state.assets.page = page;
      loadAssets();
    });
  } catch (error) {
    notify(`Failed to load assets: ${error.message}`);
  }
}

function renderAssets(items) {
  elements.assetGrid.innerHTML = '';
  items.forEach((asset) => {
    const card = document.createElement('div');
    card.className = 'asset-card';

    const img = document.createElement('img');
    img.className = 'asset-thumb';
    img.src = resolvedFileUrl(asset);
    img.alt = asset.alt_text || asset.filename;
    card.appendChild(img);

    const title = document.createElement('div');
    title.textContent = asset.original_filename || asset.filename;
    card.appendChild(title);

    const meta = document.createElement('div');
    meta.className = 'asset-meta';
    meta.textContent = `Category: ${asset.category || 'none'}`;
    card.appendChild(meta);

    const actions = document.createElement('div');
    actions.className = 'asset-actions';

    const copyBtn = document.createElement('button');
    copyBtn.className = 'btn ghost';
    copyBtn.textContent = 'Copy URL';
    copyBtn.addEventListener('click', () => copyAssetUrl(asset));

    const editBtn = document.createElement('button');
    editBtn.className = 'btn ghost';
    editBtn.textContent = 'Edit';
    editBtn.addEventListener('click', () => editAsset(asset));

    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'btn ghost';
    toggleBtn.textContent = asset.is_active ? 'Deactivate' : 'Activate';
    toggleBtn.addEventListener('click', () => toggleAsset(asset));

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn ghost';
    deleteBtn.textContent = 'Delete';
    deleteBtn.addEventListener('click', () => deleteAsset(asset.id));

    actions.appendChild(copyBtn);
    actions.appendChild(editBtn);
    actions.appendChild(toggleBtn);
    actions.appendChild(deleteBtn);
    card.appendChild(actions);

    elements.assetGrid.appendChild(card);
  });
}

async function copyAssetUrl(asset) {
  const url = resolvedFileUrl(asset);
  try {
    await navigator.clipboard.writeText(url);
    notify('URL copied');
  } catch (error) {
    notify(url);
  }
}

async function editAsset(asset) {
  const category = window.prompt('Update category', asset.category || '');
  const altText = window.prompt('Update alt text', asset.alt_text || '');
  if (category === null && altText === null) {
    return;
  }
  const formData = new FormData();
  if (category !== null) {
    formData.append('category', category);
  }
  if (altText !== null) {
    formData.append('alt_text', altText);
  }
  try {
    await apiRequest(`/api/v1/assets/${asset.id}`, { method: 'PATCH', body: formData });
    notify('Asset updated');
    addActivity(`Updated asset ${asset.id}`);
    loadAssets();
  } catch (error) {
    notify(`Update failed: ${error.message}`);
  }
}

async function toggleAsset(asset) {
  const formData = new FormData();
  formData.append('is_active', (!asset.is_active).toString());
  try {
    await apiRequest(`/api/v1/assets/${asset.id}`, { method: 'PATCH', body: formData });
    notify('Asset status updated');
    addActivity(`Toggled asset ${asset.id}`);
    loadAssets();
  } catch (error) {
    notify(`Update failed: ${error.message}`);
  }
}

async function deleteAsset(id) {
  if (!window.confirm('Delete this asset?')) {
    return;
  }
  try {
    await apiRequest(`/api/v1/assets/${id}`, { method: 'DELETE' });
    notify('Asset deleted');
    addActivity(`Deleted asset ${id}`);
    loadAssets();
  } catch (error) {
    notify(`Delete failed: ${error.message}`);
  }
}

function registerEvents() {
  elements.loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    elements.loginHint.textContent = '';
    const username = elements.loginUsername.value.trim();
    const password = elements.loginPassword.value;
    try {
      await apiRequest('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      }, false);
      setToken(username, password);
      state.user = username;
      showApp();
      await initializeApp();
    } catch (error) {
      elements.loginHint.textContent = 'Invalid credentials';
    }
  });

  elements.logoutBtn.addEventListener('click', () => {
    clearToken();
    state.user = null;
    showLogin();
  });

  elements.refreshBtn.addEventListener('click', () => {
    loadDashboard();
    if (document.getElementById('cmsView').classList.contains('active')) {
      loadCmsSection();
    }
    if (document.getElementById('newsView').classList.contains('active')) {
      loadNewsList();
    }
    if (document.getElementById('assetsView').classList.contains('active')) {
      loadAssets();
    }
  });

  document.querySelectorAll('.nav-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const view = btn.dataset.view;
      if (view === 'dashboard') {
        setView('dashboardView', 'Dashboard', 'Overview of your CMS.');
      }
      if (view === 'cms') {
        setView('cmsView', 'CMS', 'Edit structured sections.');
      }
      if (view === 'news') {
        setView('newsView', 'News', 'Manage articles and publishing.');
      }
      if (view === 'assets') {
        setView('assetsView', 'Assets', 'Upload and manage files.');
      }
      if (view === 'settings') {
        setView('settingsView', 'Settings', 'Environment and API info.');
      }
    });
  });

  elements.cmsLoadBtn.addEventListener('click', loadCmsSection);
  elements.cmsSaveBtn.addEventListener('click', saveCmsSection);

  elements.newsReloadBtn.addEventListener('click', loadNewsList);
  elements.newsNewBtn.addEventListener('click', resetNewsForm);
  elements.newsApplyFilter.addEventListener('click', () => {
    state.news.page = 1;
    loadNewsList();
  });
  elements.newsForm.addEventListener('submit', saveNews);
  elements.newsResetBtn.addEventListener('click', resetNewsForm);

  elements.assetUploadForm.addEventListener('submit', uploadAsset);
  elements.assetReloadBtn.addEventListener('click', loadAssets);

  if (elements.assetPickerClose) {
    elements.assetPickerClose.addEventListener('click', closeAssetPicker);
  }
  if (elements.assetPicker) {
    elements.assetPicker.addEventListener('click', (event) => {
      const target = event.target;
      if (target && target.hasAttribute && target.hasAttribute('data-close')) {
        closeAssetPicker();
      }
    });
  }
  if (elements.assetPickerReload) {
    elements.assetPickerReload.addEventListener('click', () => {
      state.assetPicker.page = 1;
      loadAssetPicker();
    });
  }
  if (elements.assetPickerSearch) {
    elements.assetPickerSearch.addEventListener('input', () => {
      state.assetPicker.search = elements.assetPickerSearch.value;
      renderAssetPicker();
    });
  }

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && state.assetPicker.open) {
      closeAssetPicker();
    }
  });
}

async function initializeApp() {
  renderCmsList();
  const defaultSection = cmsSections.find((section) => !section.readonly) || cmsSections[0];
  selectCmsSection(defaultSection.id);
  await loadDashboard();
  await loadNewsList();
  await loadAssets();
}

(async () => {
  registerEvents();
  const valid = await checkSession();
  if (valid) {
    showApp();
    await initializeApp();
  } else {
    showLogin();
  }
})();

