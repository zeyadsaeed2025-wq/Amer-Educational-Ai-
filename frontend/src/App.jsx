import React, { useState, useEffect, createContext } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:10000';

const AccessibilityContext = createContext({
  settings: {},
  updateSettings: () => {}
});

const modules = {
  toolbar: [
    [{ header: [1, 2, 3, false] }],
    ['bold', 'italic', 'underline', 'strike'],
    [{ list: 'ordered' }, { list: 'bullet' }],
    [{ indent: '-1' }, { indent: '+1' }],
    [{ align: [] }],
    ['link', 'image', 'video'],
    ['clean']
  ]
};

const formats = [
  'header', 'bold', 'italic', 'underline', 'strike',
  'list', 'bullet', 'indent',
  'align', 'link', 'image', 'video'
];

function apiFetch(endpoint, data = null) {
  const options = {
    method: data ? 'POST' : 'GET',
    headers: { 'Content-Type': 'application/json' }
  };
  if (data) {
    options.body = JSON.stringify(data);
  }
  return fetch(`${API_BASE}${endpoint}`, options)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .catch(error => {
      console.error('API Error:', error);
      throw error;
    });
}

function App() {
  const [view, setView] = useState('generate');
  const [accessibilitySettings, setAccessibilitySettings] = useState({
    fontSize: 'normal',
    lineSpacing: 'normal',
    highContrast: false
  });

  const updateAccessibility = (key, value) => {
    setAccessibilitySettings(prev => ({ ...prev, [key]: value }));
  };

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute('data-font-size', accessibilitySettings.fontSize === 'large' ? 'large' : accessibilitySettings.fontSize === 'xlarge' ? 'xlarge' : '');
    root.setAttribute('data-line-spacing', accessibilitySettings.lineSpacing === 'relaxed' ? 'relaxed' : '');
    root.setAttribute('data-high-contrast', accessibilitySettings.highContrast);
  }, [accessibilitySettings]);

  return (
    <AccessibilityContext.Provider value={{ settings: accessibilitySettings, updateSettings: updateAccessibility }}>
      <div className="app" dir="rtl">
        <header className="header">
          <h1>🎓EduForge AI</h1>
          <nav className="nav">
            <button className={view === 'generate' ? 'active' : ''} onClick={() => setView('generate')}>إنشاء درس</button>
            <button className={view === 'copilot' ? 'active' : ''} onClick={() => setView('copilot')}>🤖Copilot</button>
            <button className={view === 'exam' ? 'active' : ''} onClick={() => setView('exam')}>📝امتحان</button>
            <button className={view === 'lessons' ? 'active' : ''} onClick={() => setView('lessons')}>دروسي</button>
            <button className={view === 'editor' ? 'active' : ''} onClick={() => setView('editor')}>المحرر</button>
            <button className={view === 'settings' ? 'active' : ''} onClick={() => setView('settings')}>الإعدادات</button>
          </nav>
        </header>
        <main className="main">
          {view === 'generate' && <GenerateView />}
          {view === 'copilot' && <CopilotView />}
          {view === 'exam' && <ExamView />}
          {view === 'lessons' && <LessonsView />}
          {view === 'editor' && <EditorView />}
          {view === 'settings' && <SettingsView settings={accessibilitySettings} updateSettings={updateAccessibility} />}
        </main>
      </div>
    </AccessibilityContext.Provider>
  );
}

function GenerateView() {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('math');
  const [loading, setLoading] = useState(false);
  const [generated, setGenerated] = useState(null);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!title.trim()) {
      setError('الرجاء إدخال عنوان الدرس');
      return;
    }
    setLoading(true);
    setError('');
    setGenerated(null);
    
    try {
      const result = await apiFetch('/api/generate-content', { title, category });
      if (result.success) {
        setGenerated(result.data);
      } else {
        setError(result.detail || 'فشل في إنشاء المحتوى');
      }
    } catch (e) {
      setError('فشل في الاتصال بالخادم. تأكد من تشغيل الـ Backend.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!generated) return;
    try {
      await apiFetch('/api/save', {
        title,
        category,
        content: generated
      });
      alert('تم حفظ الدرس بنجاح!');
    } catch (e) {
      alert('فشل في حفظ الدرس');
    }
  };

  return (
    <div>
      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">✨ إنشاء درس بالذكاء الاصطناعي</h2>
        </div>
        <div className="form-group">
          <label htmlFor="lesson-title">عنوان الدرس</label>
          <input
            id="lesson-title"
            type="text"
            value={title}
            onChange={e => setTitle(e.target.value)}
            placeholder="مثال: مقدمة في علم النبات"
          />
        </div>
        <div className="form-group">
          <label htmlFor="category">الفئة</label>
          <select id="category" value={category} onChange={e => setCategory(e.target.value)}>
            <option value="math">الرياضيات</option>
            <option value="science">العلوم</option>
            <option value="history">التاريخ</option>
            <option value="language">اللغة العربية</option>
            <option value="geography">الجغرافيا</option>
            <option value="arts">الفنون</option>
          </select>
        </div>
        <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
          {loading ? <><span className="spinner"></span> جاري الإنشاء...</> : '✨ إنشاء الدرس'}
        </button>
        {error && <p style={{ color: 'var(--danger)', marginTop: '1rem' }}>{error}</p>}
      </div>

      {generated && (
        <ContentTabs content={generated} onSave={handleSave} />
      )}
    </div>
  );
}

function ContentTabs({ content, onSave }) {
  const [activeTab, setActiveTab] = useState('standard');
  const [editorContent, setEditorContent] = useState('');

  const tabs = [
    { id: 'standard', label: '📚 Standard' },
    { id: 'simplified', label: '📖 المبسط' },
    { id: 'accessibility', label: '♿ التسهيلات' }
  ];

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>
        <button className="btn btn-secondary" onClick={onSave}>💾 حفظ الدرس</button>
      </div>
      
      <div className="tab-content">
        {activeTab === 'standard' && <ContentDisplay content={content.standard} />}
        {activeTab === 'simplified' && <ContentDisplay content={content.simplified} />}
        {activeTab === 'accessibility' && <ContentDisplay content={content.accessibility} />}
      </div>

      <div className="editor-container" style={{ marginTop: '2rem' }}>
        <h3>✏️ تحرير المحتوى</h3>
        <ReactQuill
          theme="snow"
          value={editorContent}
          onChange={setEditorContent}
          modules={modules}
          formats={formats}
        />
      </div>
    </div>
  );
}

function ContentDisplay({ content }) {
  if (!content) return null;

  const arabicCategories = {
    'math': 'الرياضيات',
    'science': 'العلوم',
    'history': 'التاريخ',
    'language': 'اللغة',
    'geography': 'الجغرافيا',
    'arts': 'الفنون'
  };

  return (
    <div>
      <h2 style={{ marginBottom: '1rem' }}>{content.title}</h2>
      
      {content.objectives && (
        <div className="content-section">
          <h3>🎯 الأهداف التعليمية</h3>
          <ul>
            {content.objectives.map((obj, i) => (
              <li key={i}>{obj}</li>
            ))}
          </ul>
        </div>
      )}

      {content.sections && (
        <div className="content-section">
          <h3>📖 أجزاء الدرس</h3>
          {content.sections.map((section, i) => (
            <div key={i} style={{ marginBottom: '1rem' }}>
              <h4 style={{ color: 'var(--primary)' }}>{section.title}</h4>
              <p>{section.content}</p>
              {section.duration && <small style={{ color: 'var(--text-light)' }}>⏱ {section.duration}</small>}
            </div>
          ))}
        </div>
      )}

      {content.questions && (
        <div className="content-section">
          <h3>❓ الأسئلة</h3>
          <ul>
            {content.questions.map((q, i) => (
              <li key={i}><strong>{q.type}:</strong> {q.question}</li>
            ))}
          </ul>
        </div>
      )}

      {content.activities && (
        <div className="content-section">
          <h3>🎨 الأنشطة</h3>
          {content.activities.map((act, i) => (
            <div key={i} style={{ marginBottom: '0.75rem' }}>
              <strong>{act.title}</strong> - {act.description}
              <br />
              <small>النوع: {act.type} | المدة: {act.duration}</small>
            </div>
          ))}
        </div>
      )}

      {content.accessibility_features && (
        <div className="content-section accessibility-panel">
          <h3>♿ تسهيلات الوصول</h3>
          <ul>
            {Object.entries(content.accessibility_features).map(([key, value]) => (
              <li key={key}>{key}: {value === true ? 'مُفعّل' : value}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function LessonsView() {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedLesson, setSelectedLesson] = useState(null);

  useEffect(() => {
    loadLessons();
  }, []);

  const loadLessons = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiFetch('/api/lessons');
      if (result.success) {
        setLessons(result.lessons || []);
      } else {
        setError(result.detail || 'فشل في تحميل الدروس');
      }
    } catch (e) {
      console.error('فشل في تحميل الدروس:', e);
      setError('فشل في الاتصال بالخادم');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('هل أنت متأكد من حذف هذا الدرس؟')) return;
    try {
      await apiFetch(`/api/lessons/${id}`, null);
      setLessons(lessons.filter(l => l.id !== id));
      if (selectedLesson?.id === id) setSelectedLesson(null);
    } catch (e) {
      alert('فشل في حذف الدرس');
    }
  };

  if (loading) {
    return <div className="loading"><span className="spinner"></span> جاري التحميل...</div>;
  }

  if (error) {
    return (
      <div className="panel">
        <p style={{ color: 'var(--danger)' }}>{error}</p>
        <button className="btn btn-primary" onClick={loadLessons}>إعادة المحاولة</button>
      </div>
    );
  }

  if (lessons.length === 0) {
    return (
      <div className="panel">
        <p>لا توجد دروس محفوظة. أنشئ درساً واحفظه!</p>
      </div>
    );
  }

  return (
    <div>
      <div className="panel">
        <h2 className="panel-title">📁 دروسي</h2>
        {lessons.map(lesson => (
          <div key={lesson.id} className="lesson-card">
            <h3>{lesson.title}</h3>
            <p className="meta">الفئة: {lesson.category} | التاريخ: {new Date(lesson.created_at).toLocaleDateString('ar-SA')}</p>
            <div className="actions">
              <button className="btn btn-primary" onClick={() => setSelectedLesson(lesson)}>عرض</button>
              <button className="btn btn-danger" onClick={() => handleDelete(lesson.id)}>حذف</button>
            </div>
          </div>
        ))}
      </div>

      {selectedLesson && (
        <div className="panel">
          <div className="panel-header">
            <h2 className="panel-title">{selectedLesson.title}</h2>
            <button className="btn btn-secondary" onClick={() => setSelectedLesson(null)}>إغلاق</button>
          </div>
          <ContentDisplay content={selectedLesson.content} />
        </div>
      )}
    </div>
  );
}

function EditorView() {
  const [content, setContent] = useState('');
  const [correcting, setCorrecting] = useState(false);
  const [correctionResult, setCorrectionResult] = useState(null);

  const handleExport = () => {
    const blob = new Blob([content], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'lesson.html';
    a.click();
  };

  const handleCorrect = async () => {
    if (!content.trim()) {
      alert('الرجاء إدخال نص للتصحيح');
      return;
    }
    setCorrecting(true);
    try {
      const result = await apiFetch('/api/correct-content', {
        text: content
      });
      if (result.success) {
        setContent(result.corrected);
        setCorrectionResult(result);
      }
    } catch (e) {
      alert('خطأ في التصحيح');
    } finally {
      setCorrecting(false);
    }
  };

  const handleAdapt = async (mode) => {
    if (!content.trim()) return;
    try {
      const result = await apiFetch('/api/adapt-content', {
        text: content,
        mode: mode
      });
      if (result.success) {
        setContent(result.adapted);
        alert(`تم التكيف لـ ${mode === 'autism' ? 'التوحد' : mode === 'visual' ? 'ضعاف البصر' : mode === 'hearing' ? 'ضعاف السمع' : mode === 'adhd' ? 'ADHD' : 'عسر القراءة'}`);
      }
    } catch (e) {
      alert('خطأ في التكيف');
    }
  };

  return (
    <div>
      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">✏️ محرر النصوص</h2>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button className="btn btn-secondary" onClick={handleExport}>📥 تصدير</button>
          </div>
        </div>
        <p style={{ marginBottom: '1rem', color: 'var(--text-light)' }}>
          استخدم المحرر أدناه لإنشاء أو تعديل محتوى الدرس كما في Word.
        </p>
        
        <div style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button 
            className="btn btn-primary" 
            onClick={handleCorrect}
            disabled={correcting}
          >
            {correcting ? '⏳ جاري التصحيح...' : '✨ تصحيح وتحسين'}
          </button>
          <button className="btn btn-secondary" onClick={() => handleAdapt('autism')}>🧩 توحد</button>
          <button className="btn btn-secondary" onClick={() => handleAdapt('visual')}>👁️ بصر</button>
          <button className="btn btn-secondary" onClick={() => handleAdapt('hearing')}>👂 سمع</button>
          <button className="btn btn-secondary" onClick={() => handleAdapt('adhd')}>🟡 ADHD</button>
          <button className="btn btn-secondary" onClick={() => handleAdapt('dyslexia')}>📝 عسر قراءة</button>
        </div>

        {correctionResult && (
          <div style={{ padding: '1rem', background: '#e8f5e9', borderRadius: '8px', marginBottom: '1rem' }}>
            <h4>📊 نتائج التصحيح:</h4>
            <ul>
              {correctionResult.improvements?.map((imp, i) => (
                <li key={i}>{imp}</li>
              ))}
            </ul>
          </div>
        )}
        
        <ReactQuill
          theme="snow"
          value={content}
          onChange={setContent}
          modules={modules}
          formats={formats}
          style={{ minHeight: '400px' }}
        />
      </div>
    </div>
  );
}

function SettingsView({ settings, updateSettings }) {
  return (
    <div>
      <div className="panel">
        <h2 className="panel-title">⚙️ إعدادات التسهيلات</h2>
        
        <div className="form-group">
          <label>حجم الخط</label>
          <select 
            value={settings.fontSize} 
            onChange={e => updateSettings('fontSize', e.target.value)}
          >
            <option value="normal">عادي</option>
            <option value="large">كبير</option>
            <option value="xlarge">كبير جداً</option>
          </select>
        </div>

        <div className="form-group">
          <label>تباعد الأسطر</label>
          <select 
            value={settings.lineSpacing}
            onChange={e => updateSettings('lineSpacing', e.target.value)}
          >
            <option value="normal">عادي</option>
            <option value="relaxed">متباعد</option>
          </select>
        </div>

        <div className="form-group">
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              checked={settings.highContrast}
              onChange={e => updateSettings('highContrast', e.target.checked)}
            />
            وضع التباين العالي
          </label>
        </div>
      </div>

      <div className="panel">
        <h2 className="panel-title">🔐 المصادقة</h2>
        <p style={{ color: 'var(--text-light)', marginBottom: '1rem' }}>
         连接 إلى Supabase للمصادقة والمزامنة السحابية.
        </p>
        <div className="form-group">
          <label>رابط Supabase</label>
          <input type="text" placeholder="https://your-project.supabase.co" />
        </div>
        <div className="form-group">
          <label>مفتاح Supabase</label>
          <input type="password" placeholder="المفتاح السري" />
        </div>
        <button className="btn btn-primary">اتصال</button>
      </div>
    </div>
  );
}

function CopilotView() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('student');
  const [disability, setDisability] = useState('none');
  const [showQuickActions, setShowQuickActions] = useState(true);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage = input;
    setInput('');
    setLoading(true);
    setShowQuickActions(false);
    
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    try {
      const result = await apiFetch('/api/copilot-chat', {
        message: userMessage,
        mode: mode,
        disability: disability
      });
      
      if (result.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: result.reply }]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: 'عذراً، حدث خطأ. حاول مرة أخرى.' }]);
      }
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'عذراً، لم أتمكن من الاتصال بالخادم.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = async (action) => {
    setLoading(true);
    setShowQuickActions(false);
    
    let prompt = '';
    switch(action) {
      case 'explain':
        prompt = 'أريد شرح مفهوم جديد';
        break;
      case 'quiz':
        prompt = 'أنشئ اختبار قصير';
        break;
      case 'simplify':
        prompt = 'بسّط هذا الشرح';
        break;
      case 'tutor':
        prompt = 'فهمني هذا الدرس خطوة بخطوة';
        break;
      default:
        prompt = action;
    }
    
    setInput(prompt);
    setLoading(false);
  };

  const clearChat = () => {
    setMessages([]);
    setShowQuickActions(true);
  };

  return (
    <div className="copilot-container">
      <div className="panel copilot-panel">
        <div className="panel-header">
          <h2 className="panel-title">🤖 EduForge Copilot</h2>
          <button className="btn btn-secondary" onClick={clearChat}>🗑️ جديد</button>
        </div>
        
        <div className="copilot-modes">
          <div className="mode-selector">
            <label>الوضع:</label>
            <select value={mode} onChange={e => setMode(e.target.value)}>
              <option value="student">🎓 طالب</option>
              <option value="teacher">👨‍🏫 معلم</option>
            </select>
          </div>
          
          <div className="disability-selector">
            <label>التسهيلات:</label>
            <select value={disability} onChange={e => setDisability(e.target.value)}>
              <option value="none">👤 عادي</option>
              <option value="autism">🔵 توحد</option>
              <option value="adhd">🟡 ADHD</option>
              <option value="dyslexia">📝 عسر قراءة</option>
              <option value="blind">👁️ كفيف</option>
              <option value="deaf">🔊 أصم</option>
            </select>
          </div>
        </div>

        <div className="chat-container">
          {messages.length === 0 && showQuickActions && (
            <div className="quick-actions">
              <p>💡 كيف يمكنني مساعدتك؟</p>
              <div className="action-buttons">
                <button onClick={() => handleQuickAction('explain')}>📖 شرح درس</button>
                <button onClick={() => handleQuickAction('quiz')}>📝 إنشاء اختبار</button>
                <button onClick={() => handleQuickAction('simplify')}>🔰 تبسيط</button>
                <button onClick={() => handleQuickAction('tutor')}>👨‍🏫 مدرس خصوصي</button>
              </div>
            </div>
          )}
          
          <div className="messages">
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                <div className="message-role">{msg.role === 'user' ? '👤 أنت' : '🤖 Copilot'}</div>
                <div className="message-content">{msg.content}</div>
              </div>
            ))}
            {loading && <div className="message assistant"><div className="message-role">🤖 Copilot</div><div className="message-content">جاري الكتابة... ⏳</div></div>}
          </div>
        </div>

        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && handleSend()}
            placeholder="اسأل سؤالاً تعليمياً..."
            disabled={loading}
          />
          <button className="btn btn-primary" onClick={handleSend} disabled={loading || !input.trim()}>
            {loading ? '...' : 'إرسال'}
          </button>
        </div>
      </div>
    </div>
  );
}

function ExamView() {
  const [topic, setTopic] = useState('');
  const [level, setLevel] = useState('medium');
  const [category, setCategory] = useState('standard');
  const [count, setCount] = useState(10);
  const [exam, setExam] = useState(null);
  const [loading, setLoading] = useState(false);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  const handleGenerate = async () => {
    if (!topic.trim()) {
      alert('الرجاء إدخال موضوع الاختبار');
      return;
    }
    setLoading(true);
    setExam(null);
    setResult(null);
    setAnswers({});
    
    try {
      const response = await apiFetch('/api/generate-exam', {
        topic,
        level,
        category,
        count
      });
      
      if (response.success) {
        setExam(response.exam);
      } else {
        alert('فشل في إنشاء الاختبار');
      }
    } catch (e) {
      alert('خطأ في الاتصال');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (type, id, value) => {
    setAnswers(prev => ({ ...prev, [`${type}_${id}`]: value }));
  };

  const handleSubmitExam = async () => {
    if (!exam) return;
    
    try {
      const response = await apiFetch('/api/grade-exam', {
        answers,
        exam
      });
      
      if (response.success) {
        setResult(response);
      }
    } catch (e) {
      alert('خطأ في التصحيح');
    }
  };

  const resetExam = () => {
    setExam(null);
    setAnswers({});
    setResult(null);
  };

  return (
    <div>
      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">📝 نظام الامتحانات AI</h2>
        </div>
        
        {!exam && (
          <div>
            <div className="form-group">
              <label>موضوع الاختبار</label>
              <input
                type="text"
                value={topic}
                onChange={e => setTopic(e.target.value)}
                placeholder="مثال: الرياضيات، التاريخ، العلوم"
              />
            </div>
            
            <div className="form-group">
              <label>مستوى الصعوبة</label>
              <select value={level} onChange={e => setLevel(e.target.value)}>
                <option value="beginner">مبتدئ</option>
                <option value="medium">متوسط</option>
                <option value="advanced">متقدم</option>
              </select>
            </div>
            
            <div className="form-group">
              <label>الفئة</label>
              <select value={category} onChange={e => setCategory(e.target.value)}>
                <option value="standard">عادي</option>
                <option value="autism">توحد</option>
                <option value="adhd">ADHD</option>
                <option value="dyslexia">عسر قراءة</option>
                <option value="blind">كفيف</option>
                <option value="deaf">أصم</option>
              </select>
            </div>
            
            <div className="form-group">
              <label>عدد الأسئلة</label>
              <input
                type="number"
                value={count}
                onChange={e => setCount(parseInt(e.target.value) || 10)}
                min={5}
                max={50}
              />
            </div>
            
            <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
              {loading ? 'جاري الإنشاء...' : '🎯 إنشاء اختبار'}
            </button>
          </div>
        )}
        
        {exam && exam.error && (
          <div className="panel" style={{ background: '#fee', padding: '1rem' }}>
            <p>حدث خطأ في إنشاء الاختبار. جرب مرة أخرى.</p>
            <button className="btn btn-secondary" onClick={resetExam}>إعادة المحاولة</button>
          </div>
        )}
        
        {exam && !exam.error && (
          <div>
            <div className="panel-header">
              <h3>📋 {exam.exam_title || `اختبار ${exam.topic}`}</h3>
              <button className="btn btn-secondary" onClick={resetExam}>امتحان جديد</button>
            </div>
            
            {exam.mcq && exam.mcq.length > 0 && (
              <div className="content-section">
                <h4>📌 أسئلة الاختيار من متعدد</h4>
                {exam.mcq.map((q, i) => (
                  <div key={q.id} style={{ marginBottom: '1.5rem', padding: '1rem', background: 'var(--background)', borderRadius: '8px' }}>
                    <p><strong>{i+1}.</strong> {q.question}</p>
                    {q.options.map((opt, j) => (
                      <label key={j} style={{ display: 'block', margin: '0.5rem 0', cursor: 'pointer' }}>
                        <input
                          type="radio"
                          name={`mcq_${q.id}`}
                          value={String.fromCharCode(65 + j)}
                          onChange={() => handleAnswerChange('mcq', q.id, String.fromCharCode(65 + j))}
                        /> {opt}
                      </label>
                    ))}
                  </div>
                ))}
              </div>
            )}
            
            {exam.true_false && exam.true_false.length > 0 && (
              <div className="content-section">
                <h4>✓ صح أو خطأ</h4>
                {exam.true_false.map((q, i) => (
                  <div key={q.id} style={{ marginBottom: '1rem', padding: '1rem', background: 'var(--background)', borderRadius: '8px' }}>
                    <p><strong>{i+1}.</strong> {q.question}</p>
                    <select
                      value={answers[`tf_${q.id}`] || ''}
                      onChange={e => handleAnswerChange('tf', q.id, e.target.value)}
                    >
                      <option value="">اختر...</option>
                      <option value="true">صح</option>
                      <option value="false">خطأ</option>
                    </select>
                  </div>
                ))}
              </div>
            )}
            
            {exam.short_answers && exam.short_answers.length > 0 && (
              <div className="content-section">
                <h4>✏️ أسئلة قصيرة</h4>
                {exam.short_answers.map((q, i) => (
                  <div key={q.id} style={{ marginBottom: '1rem' }}>
                    <p><strong>{i+1}.</strong> {q.question}</p>
                    <textarea
                      style={{ width: '100%', minHeight: '80px', padding: '0.5rem' }}
                      placeholder="اكتب إجابتك هنا..."
                      value={answers[`sa_${q.id}`] || ''}
                      onChange={e => handleAnswerChange('sa', q.id, e.target.value)}
                    />
                  </div>
                ))}
              </div>
            )}
            
            {!result && (
              <button className="btn btn-primary" onClick={handleSubmitExam}>
                📊 تسليم الإجابات وتصحيح
              </button>
            )}
            
            {result && (
              <div className="panel" style={{ background: result.score >= 70 ? '#d4edda' : '#f8d7da', marginTop: '1rem' }}>
                <h3>📊 النتيجة</h3>
                <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>
                  {result.score}%
                </p>
                <p>الإجابات الصحيحة: {result.correct} / {result.total}</p>
                <p>{result.message}</p>
                
                <div style={{ marginTop: '1rem' }}>
                  <h4>التفاصيل:</h4>
                  {result.feedback.map((f, i) => (
                    <p key={i} style={{ fontSize: '0.9rem' }}>{f}</p>
                  ))}
                </div>
                
                <button className="btn btn-secondary" onClick={resetExam} style={{ marginTop: '1rem' }}>
                  امتحان جديد
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;