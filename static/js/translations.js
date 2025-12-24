// NETRA Translation System
// Supports: ID, EN, ZH-TW, ZH-CN, VI, JA

const translations = {
    // Indonesian (Default)
    'id': {
        // Navbar
        'nav.home': 'Beranda',
        'nav.ocr': 'OCR Scan',
        'nav.document': 'Parse Document',
        'nav.batch': 'Batch',
        'nav.alltools': 'All Tools',
        'nav.more': 'More',
        'nav.more': 'Lainnya',
        'nav.login': 'Login',
        'nav.signup': 'Sign up',
        'nav.logout': 'Logout',

        // Hero
        'hero.badge': 'Powered by OCR & Rabin-Karp',
        'hero.title': 'Asisten untuk',
        'hero.highlight_keyword': 'Review Tinjauan Pustaka',
        'hero.suffix': 'Anda',
        'hero.description': 'Tak perlu baca satu per satu. Upload dokumen Anda, biarkan kami menemukan bagian yang relevan untuk riset Anda secara instan.',
        'hero.btn.ocr': 'Mulai OCR Scan',
        'hero.btn.document': 'Parse Document',

        // Features
        'features.title': 'Fitur Unggulan',
        'features.subtitle': 'Tools lengkap untuk analisis dokumen akademis Anda',
        'features.ocr.title': 'OCR Scan',
        'features.ocr.desc': 'Ekstrak teks dari gambar dengan akurasi tinggi menggunakan Tesseract OCR.',
        'features.document.title': 'Document Parser',
        'features.document.desc': 'Parse dokumen PDF dan DOCX untuk ekstraksi teks otomatis.',
        'features.batch.title': 'Batch Analysis',
        'features.batch.desc': 'Analisis multiple dokumen sekaligus dengan efisien.',
        'features.rabinkarp.title': 'Rabin-Karp',
        'features.rabinkarp.desc': 'Algoritma pencarian string dengan rolling hash untuk analisis relevansi.',

        // Stats
        'stats.documents': 'Dokumen Diproses',
        'stats.accuracy': 'Akurasi OCR',
        'stats.time': 'Waktu Proses',
        'stats.rating': 'Rating User',

        // FAQ
        'faq.title': 'Pertanyaan Umum',
        'faq.subtitle': 'Temukan jawaban untuk pertanyaan yang sering diajukan',

        // Footer
        'footer.tools': 'TOOLS',
        'footer.company': 'COMPANY',
        'footer.legal': 'LEGAL',
        'footer.privacy': 'Kebijakan Privasi',
        'footer.terms': 'Syarat & Ketentuan',
        'footer.about': 'About',
        'footer.pricing': 'Pricing',
        'footer.contact': 'Contact',
        'footer.copyright': '© 2025 NETRA. All rights reserved.',

        // Common
        'common.register': 'Daftar Sekarang',
        'common.loading': 'Memuat...',
        'common.error': 'Terjadi kesalahan'
    },

    // English
    'en': {
        'nav.home': 'Home',
        'nav.ocr': 'OCR Scan',
        'nav.document': 'Parse Document',
        'nav.batch': 'Batch',
        'nav.alltools': 'All Tools',
        'nav.more': 'More',
        'nav.login': 'Login',
        'nav.signup': 'Sign up',
        'nav.logout': 'Logout',

        'hero.badge': 'Powered by OCR & Rabin-Karp',
        'hero.title': 'Assistant for',
        'hero.highlight_keyword': 'Your Literature Review',
        'hero.suffix': '',
        'hero.description': 'No need to read one by one. Upload your documents, let us find the relevant parts for your research instantly.',
        'hero.btn.ocr': 'Start OCR Scan',
        'hero.btn.document': 'Parse Document',

        'features.title': 'Key Features',
        'features.subtitle': 'Complete tools for your academic document analysis',
        'features.ocr.title': 'OCR Scan',
        'features.ocr.desc': 'Extract text from images with high accuracy using Tesseract OCR.',
        'features.document.title': 'Document Parser',
        'features.document.desc': 'Parse PDF and DOCX documents for automatic text extraction.',
        'features.batch.title': 'Batch Analysis',
        'features.batch.desc': 'Analyze multiple documents at once efficiently.',
        'features.rabinkarp.title': 'Rabin-Karp',
        'features.rabinkarp.desc': 'String search algorithm with rolling hash for relevance analysis.',

        'stats.documents': 'Documents Processed',
        'stats.accuracy': 'OCR Accuracy',
        'stats.time': 'Processing Time',
        'stats.rating': 'User Rating',

        'faq.title': 'Frequently Asked Questions',
        'faq.subtitle': 'Find answers to commonly asked questions',

        'footer.tools': 'TOOLS',
        'footer.company': 'COMPANY',
        'footer.legal': 'LEGAL',
        'footer.privacy': 'Privacy Policy',
        'footer.terms': 'Terms & Conditions',
        'footer.about': 'About',
        'footer.pricing': 'Pricing',
        'footer.contact': 'Contact',
        'footer.copyright': '© 2025 NETRA. All rights reserved.',

        'common.register': 'Register Now',
        'common.loading': 'Loading...',
        'common.error': 'An error occurred'
    },

    // Chinese Traditional
    'zh-TW': {
        'nav.home': '首頁',
        'nav.ocr': 'OCR掃描',
        'nav.document': '文件解析',
        'nav.batch': '批量處理',
        'nav.alltools': '所有工具',
        'nav.login': '登入',
        'nav.signup': '註冊',
        'nav.logout': '登出',

        'hero.badge': 'Powered by OCR & Rabin-Karp',
        'hero.title': '您文獻回顧的',
        'hero.highlight_keyword': '最佳助手',
        'hero.suffix': '',
        'hero.description': '無需逐一閱讀。上傳您的文件，讓我們立即為您的研究找到相關部分。',
        'hero.btn.ocr': '開始OCR掃描',
        'hero.btn.document': '解析文件',

        'features.title': '主要功能',
        'features.subtitle': '學術文件分析的完整工具',
        'features.ocr.title': 'OCR掃描',
        'features.ocr.desc': '使用Tesseract OCR高精度提取圖像文字。',
        'features.document.title': '文件解析器',
        'features.document.desc': '解析PDF和DOCX文件以自動提取文字。',
        'features.batch.title': '批量分析',
        'features.batch.desc': '高效同時分析多個文件。',
        'features.rabinkarp.title': 'Rabin-Karp',
        'features.rabinkarp.desc': '用於相關性分析的滾動哈希字符串搜索算法。',

        'stats.documents': '已處理文件',
        'stats.accuracy': 'OCR準確度',
        'stats.time': '處理時間',
        'stats.rating': '用戶評分',

        'faq.title': '常見問題',
        'faq.subtitle': '查找常見問題的答案',

        'footer.tools': '工具',
        'footer.company': '公司',
        'footer.legal': '法律',
        'footer.privacy': '隱私政策',
        'footer.terms': '條款和條件',
        'footer.about': '關於',
        'footer.pricing': '價格',
        'footer.contact': '聯繫',
        'footer.copyright': '© 2025 NETRA. 版權所有。',

        'common.register': '立即註冊',
        'common.loading': '載入中...',
        'common.error': '發生錯誤'
    },

    // Chinese Simplified
    'zh-CN': {
        'nav.home': '首页',
        'nav.ocr': 'OCR扫描',
        'nav.document': '文件解析',
        'nav.batch': '批量处理',
        'nav.alltools': '所有工具',
        'nav.login': '登录',
        'nav.signup': '注册',
        'nav.logout': '退出',

        'hero.badge': 'Powered by OCR & Rabin-Karp',
        'hero.title': '您文献回顾的',
        'hero.highlight_keyword': '最佳助手',
        'hero.suffix': '',
        'hero.description': '无需逐一阅读。上传您的文档，让我们立即为您的研究找到相关部分。',
        'hero.btn.ocr': '开始OCR扫描',
        'hero.btn.document': '解析文档',

        'features.title': '主要功能',
        'features.subtitle': '学术文档分析的完整工具',
        'features.ocr.title': 'OCR扫描',
        'features.ocr.desc': '使用Tesseract OCR高精度提取图像文字。',
        'features.document.title': '文档解析器',
        'features.document.desc': '解析PDF和DOCX文档以自动提取文字。',
        'features.batch.title': '批量分析',
        'features.batch.desc': '高效同时分析多个文档。',
        'features.rabinkarp.title': 'Rabin-Karp',
        'features.rabinkarp.desc': '用于相关性分析的滚动哈希字符串搜索算法。',

        'stats.documents': '已处理文档',
        'stats.accuracy': 'OCR准确度',
        'stats.time': '处理时间',
        'stats.rating': '用户评分',

        'faq.title': '常见问题',
        'faq.subtitle': '查找常见问题的答案',

        'footer.tools': '工具',
        'footer.company': '公司',
        'footer.legal': '法律',
        'footer.privacy': '隐私政策',
        'footer.terms': '条款和条件',
        'footer.about': '关于',
        'footer.pricing': '价格',
        'footer.contact': '联系',
        'footer.copyright': '© 2025 NETRA. 版权所有。',

        'common.register': '立即注册',
        'common.loading': '加载中...',
        'common.error': '发生错误'
    },

    // Vietnamese
    'vi': {
        'nav.home': 'Trang chủ',
        'nav.ocr': 'Quét OCR',
        'nav.document': 'Phân tích tài liệu',
        'nav.batch': 'Xử lý hàng loạt',
        'nav.alltools': 'Tất cả công cụ',
        'nav.login': 'Đăng nhập',
        'nav.signup': 'Đăng ký',
        'nav.logout': 'Đăng xuất',

        'hero.badge': 'Powered by OCR & Rabin-Karp',
        'hero.title': 'Trợ lý cho',
        'hero.highlight_keyword': 'Đánh giá Tài liệu',
        'hero.suffix': 'của bạn',
        'hero.description': 'Không cần đọc từng tài liệu. Tải lên tài liệu của bạn, hãy để chúng tôi tìm phần liên quan cho nghiên cứu của bạn ngay lập tức.',
        'hero.btn.ocr': 'Bắt đầu quét OCR',
        'hero.btn.document': 'Phân tích tài liệu',

        'features.title': 'Tính năng chính',
        'features.subtitle': 'Công cụ hoàn chỉnh cho phân tích tài liệu học thuật của bạn',
        'features.ocr.title': 'Quét OCR',
        'features.ocr.desc': 'Trích xuất văn bản từ hình ảnh với độ chính xác cao sử dụng Tesseract OCR.',
        'features.document.title': 'Phân tích tài liệu',
        'features.document.desc': 'Phân tích tài liệu PDF và DOCX để trích xuất văn bản tự động.',
        'features.batch.title': 'Phân tích hàng loạt',
        'features.batch.desc': 'Phân tích nhiều tài liệu cùng lúc một cách hiệu quả.',
        'features.rabinkarp.title': 'Rabin-Karp',
        'features.rabinkarp.desc': 'Thuật toán tìm kiếm chuỗi với băm cuộn để phân tích mức độ liên quan.',

        'stats.documents': 'Tài liệu đã xử lý',
        'stats.accuracy': 'Độ chính xác OCR',
        'stats.time': 'Thời gian xử lý',
        'stats.rating': 'Đánh giá người dùng',

        'faq.title': 'Câu hỏi thường gặp',
        'faq.subtitle': 'Tìm câu trả lời cho các câu hỏi thường gặp',

        'footer.tools': 'CÔNG CỤ',
        'footer.company': 'CÔNG TY',
        'footer.legal': 'PHÁP LÝ',
        'footer.privacy': 'Chính sách bảo mật',
        'footer.terms': 'Điều khoản & Điều kiện',
        'footer.about': 'Giới thiệu',
        'footer.pricing': 'Bảng giá',
        'footer.contact': 'Liên hệ',
        'footer.copyright': '© 2025 NETRA. Bảo lưu mọi quyền.',

        'common.register': 'Đăng ký ngay',
        'common.loading': 'Đang tải...',
        'common.error': 'Đã xảy ra lỗi'
    },

    // Japanese
    'ja': {
        'nav.home': 'ホーム',
        'nav.ocr': 'OCRスキャン',
        'nav.document': 'ドキュメント解析',
        'nav.batch': 'バッチ処理',
        'nav.alltools': 'すべてのツール',
        'nav.login': 'ログイン',
        'nav.signup': '新規登録',
        'nav.logout': 'ログアウト',

        'hero.badge': 'Powered by OCR & Rabin-Karp',
        'hero.title': 'あなたの',
        'hero.highlight_keyword': '文献レビュー',
        'hero.suffix': 'のアシスタント',
        'hero.description': '一つずつ読む必要はありません。ドキュメントをアップロードして、研究に関連する部分を即座に見つけましょう。',
        'hero.btn.ocr': 'OCRスキャン開始',
        'hero.btn.document': 'ドキュメント解析',

        'features.title': '主な機能',
        'features.subtitle': '学術文書分析のための完全なツール',
        'features.ocr.title': 'OCRスキャン',
        'features.ocr.desc': 'Tesseract OCRを使用して画像から高精度でテキストを抽出。',
        'features.document.title': 'ドキュメントパーサー',
        'features.document.desc': 'PDFおよびDOCXドキュメントを解析して自動テキスト抽出。',
        'features.batch.title': 'バッチ分析',
        'features.batch.desc': '複数のドキュメントを効率的に同時分析。',
        'features.rabinkarp.title': 'Rabin-Karp',
        'features.rabinkarp.desc': '関連性分析のためのローリングハッシュ文字列検索アルゴリズム。',

        'stats.documents': '処理済み文書',
        'stats.accuracy': 'OCR精度',
        'stats.time': '処理時間',
        'stats.rating': 'ユーザー評価',

        'faq.title': 'よくある質問',
        'faq.subtitle': 'よくある質問への回答を見つける',

        'footer.tools': 'ツール',
        'footer.company': '会社',
        'footer.legal': '法的情報',
        'footer.privacy': 'プライバシーポリシー',
        'footer.terms': '利用規約',
        'footer.about': '会社概要',
        'footer.pricing': '料金',
        'footer.contact': 'お問い合わせ',
        'footer.copyright': '© 2025 NETRA. All rights reserved.',

        'common.register': '今すぐ登録',
        'common.loading': '読み込み中...',
        'common.error': 'エラーが発生しました'
    }
};

// Translation function
function t(key) {
    const lang = localStorage.getItem('netra-lang') || 'id';
    return translations[lang]?.[key] || translations['id'][key] || key;
}

// Apply translations to page
function applyTranslations() {
    const lang = localStorage.getItem('netra-lang') || 'id';
    const langData = translations[lang] || translations['id'];

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (langData[key]) {
            el.textContent = langData[key];
        }
    });

    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (langData[key]) {
            el.placeholder = langData[key];
        }
    });

    // Update page lang attribute
    document.documentElement.lang = lang === 'zh-TW' || lang === 'zh-CN' ? 'zh' : lang;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', applyTranslations);

// Export for use in other scripts
window.netraI18n = {
    t,
    applyTranslations,
    translations
};

