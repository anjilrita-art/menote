
 // Tab switching functionality
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.target.getAttribute('data-tab');
                
                // Hide all tabs
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // Remove active class from all buttons
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                
                // Show selected tab
                document.getElementById(tab).classList.add('active');
                
                // Add active class to clicked button
                e.target.classList.add('active');
            });
        });

        // If you open this HTML via VSCode Live Server or file://, the API may be on a different origin.
        // You can also force it with `?api=http://127.0.0.1:8000`.
        const API_BASE = (() => {
            const params = new URLSearchParams(window.location.search || '');
            const fromQuery = (params.get('api') || '').trim();
            if (fromQuery) return fromQuery.replace(/\/+$/, '');
            if (window.location.protocol === 'file:') return 'http://127.0.0.1:8000';
            // If you're already on the Flask server (served from /), use same-origin.
            if (window.location.port === '8000') return '';
            // Common dev setup: Live Server on 5500, Flask on 8000.
            return 'http://127.0.0.1:8000';
        })();
        const FACULTIES = ['BEL', 'BCT', 'BEX', 'BMX', 'BCE'];
        const SEMESTERS = ['1','2','3','4','5','6','7','8'];

        const SUBJECTS_BY_FAC_SEM = {
            BEL: {
                '1': [
                    'Engineering Mathematics I',
                    'Engineering Physics',
                    'Computer Programming',
                    'Engineering Drawing',
                    'Applied Mechanics',
                    'Electric Circuit I'
                ],
                '2': [
                    'Engineering Mathematics II',
                    'Engineering Chemistry',
                    'Electronics Circuits',
                    'Advanced Computer Programming',
                    'Electric Circuit II',
                    'Electrical Installation Workshop'
                ],
                '3': [
                    'Engineering Mathematics III',
                    'Instrumentation and Measurement',
                    'Electrical Machine I',
                    'Electrical Engineering Material',
                    'Power System Analysis I',
                    'Logic circuit'
                ],
                '4': [
                    'Communication English',
                    'Numerical Methods',
                    'Probability and Statistics',
                    'Microprocessors and Microcontrollers',
                    'Control System',
                    'Power System Analysis II',
                    'Electric Machine II'
                ],
                '5': [
                    'Digital Signal Processing and Application',
                    'Engineering Thermodynamics and Heat Transfer',
                    'Project Engineering and Management',
                    'Power Electronics',
                    'Digital Control System',
                    'Switchgear and Protection',
                    'Electric Machine Design'
                ],
                '6': [
                    'Engineering Economics',
                    'Industrial Instrumentation and Automation',
                    'Industrial Electrification',
                    'Electrical Drives',
                    'Electric Power Distribution System',
                    'Minor Project',
                    'Elective I'
                ],
                '7': [
                    'Power Plant Engineering',
                    'Power System Operation and Control',
                    'High Voltage Engineering',
                    'Transmission System Design',
                    'Elective II',
                    'Elective III',
                    'Project I'
                ],
                '8': [
                    'Engineering Profession and Society',
                    'Internship',
                    'Project II'
                ]
            },
            BCT: {
                '1': [
                    'Engineering Mathematics I',
                    'Engineering Physics',
                    'Computer Programming',
                    'Engineering Drawing',
                    'Engineering Workshop',
                    'Fundamental of Electrical and Electronics Engineering'
                ],
                '2': [
                    'Engineering Mathematics II',
                    'Engineering Chemistry',
                    'Object Oriented Programming',
                    'Digital Logic',
                    'Electronic Device and Circuits',
                    'Electrical Circuits and Machines'
                ],
                '3': [
                    'Engineering Mathematics III',
                    'Communication English',
                    'Computer Graphics and Visualization',
                    'Foundation of Data Science',
                    'Theory of Computation',
                    'Microprocessors'
                ],
                '4': [
                    'Numerical Methods',
                    'Instrumentation',
                    'Electromagnetics',
                    'Data Structure and Algorithm',
                    'Data Communication',
                    'Operating System'
                ],
                '5': [
                    'Probability and Statistics',
                    'Database Management System',
                    'Web Application Programming',
                    'Computer Organization and Architecture',
                    'Computer Networks',
                    'Elective I'
                ],
                '6': [
                    'Engineering Economics',
                    'Artificial Intelligence',
                    'Software Engineering',
                    'Simulation and Modeling',
                    'Minor Project',
                    'Elective II'
                ],
                '7': [
                    'Digital Signal Analysis and Processing',
                    'Distributed and Cloud Computing',
                    'ICT Project Management',
                    'Energy, Environment and Social Engineering',
                    'Elective III',
                    'Project I'
                ],
                '8': [
                    'Network and Cyber Security',
                    'Elective IV',
                    'Internship',
                    'Project II'
                ]
            },
            BCE: {
                '1': [
                    'Engineering Mathematics I',
                    'Engineering Chemistry',
                    'Computer Programming',
                    'Basic Electrical and Electronics Engineering',
                    'Engineering Mechanics',
                    'Engineering Geology I',
                    'Civil Engineering Materials'
                ],
                '2': [
                    'Engineering Mathematics II',
                    'Engineering Physics',
                    'Engineering Drawing',
                    'Strength of Materials',
                    'Engineering Geology II',
                    'Engineering Survey I'
                ],
                '3': [
                    'Engineering Mathematics III',
                    'Numerical Methods',
                    'Fluid Mechanics',
                    'Theory of Structures I',
                    'Engineering Survey II',
                    'Computer Aided Civil Drawing',
                    'Concrete Technology'
                ],
                '4': [
                    'Communication English',
                    'Probability and Statistics',
                    'Hydraulics',
                    'Theory of Structures II',
                    'Soil Mechanics',
                    'Water Supply Engineering',
                    'Building Technology',
                    'Survey Camp'
                ],
                '5': [
                    'Design of Timber and Masonry Structures',
                    'Foundation Engineering',
                    'Design of Steel Structures',
                    'Transportation Engineering I',
                    'Sanitary Engineering',
                    'Engineering Hydrology',
                    'Engineering Economics'
                ],
                '6': [
                    'Estimating and Costing',
                    'Design of RCC Structures',
                    'Transportation Engineering II',
                    'Irrigation and Drainage Engineering',
                    'Professional and Social Engineering',
                    'Elective I'
                ],
                '7': [
                    'Operations Research',
                    'Project and Construction Engineering',
                    'Hydropower Engineering',
                    'Elective II',
                    'Elective III',
                    'Project I'
                ],
                '8': [
                    'Project II',
                    'Internship'
                ]
            }
            ,
            BEX: {
                '1': [
                    'Computer Programming',
                    'Engineering Drawing',
                    'Engineering Mathematics I',
                    'Engineering Physics',
                    'Engineering Workshop',
                    'Fundamental of Electrical and Electronics Engineering'
                ],
                '2': [
                    'Digital Logic',
                    'Electrical Circuits and Machines',
                    'Electronic Device and Circuits',
                    'Engineering Chemistry',
                    'Engineering Mathematics II',
                    'Object Oriented Programming'
                ],
                '3': [
                    'Advanced Electronics',
                    'Communication English',
                    'Computer Graphics and Visualization',
                    'Control System',
                    'Engineering Mathematics III',
                    'Microprocessors'
                ],
                '4': [
                    'Computer Organization & Architecture',
                    'Discrete Structure',
                    'Electromagnetics',
                    'Instrumentation',
                    'Numerical Methods',
                    'Signals and Systems'
                ],
                '5': [
                    'Artificial Intelligence',
                    'Elective I',
                    'Embedded Systems',
                    'Filter Design',
                    'Probability and Statistics',
                    'Propogation and Antennna'
                ],
                '6': [
                    'Communication Systems',
                    'Elective II',
                    'Engineering Economics',
                    'ICT Project Management',
                    'Minor Project',
                    'Telecommunication and Computer Networks'
                ],
                '7': [
                    'Digital Signal Processing',
                    'Elective III',
                    'Project I',
                    'RF and Microwave Engineering',
                    'Robotics',
                    'Wireless Communication'
                ],
                '8': [
                    'Elective IV',
                    'Energy, Environment and Social Engineering',
                    'Internship**',
                    'Project II'
                ]
            },
            BMX: {
                '1': [
                    'Computer Programming',
                    'Engineering Chemistry',
                    'Engineering Drawing',
                    'Engineering Mathematics I',
                    'Engineering Mechanics I',
                    'Fundamental of Electrical and Electronics Engineering'
                ],
                '2': [
                    'Engineering Mathematics II',
                    'Engineering Mechanics II',
                    'Engineering Physics',
                    'Engineering Thermodynamics I',
                    'Machine Drawing',
                    'Workshop Technology'
                ],
                '3': [
                    'Engineering Mathematics III',
                    'Engineering Thermodynamics II',
                    'Manufacturing and Production Processes',
                    'Material Science',
                    'Metrology',
                    'Strength of Materials'
                ],
                '4': [
                    'Computer Aided Design',
                    'Electrical Machines',
                    'Fluid Mechanics with Engineering Applications',
                    'Instrumentation and Sensors',
                    'Mechanics of Solids',
                    'Probability and Statistics'
                ],
                '5': [
                    'Automotive Technology',
                    'Control System and Automation',
                    'Fluid Machines',
                    'Numerical Methods',
                    'Organization and Management',
                    'Technical English',
                    'Theory of Machines and Mechanism'
                ],
                '6': [
                    'Elective I',
                    'Heat and Mass Transfer',
                    'Industrial Engineering and Management',
                    'Machine Design I',
                    'Machine Dynamics',
                    'Minor Project',
                    'Professional Engineering Economics'
                ],
                '7': [
                    'Applied Computational Fluid Dynamics',
                    'Elective II',
                    'Energy Resources and Technology',
                    'Enterpreneurship Development',
                    'Finite Element Method',
                    'Machine Design II',
                    'Project I'
                ],
                '8': [
                    'Elective III',
                    'Industrial Attachment*',
                    'Project II',
                    'Project Management and Professional Practice'
                ]
            }
        };
        let a = 1; 

        
        let notesCache = [];
        let selectedFaculty = 'BEL';
        let selectedSemester = '1';
        let selectedSubject = '__all__';
        let notesSearchQuery = '';

        let papersCache = [];
        let papersFaculty = 'BEL';
        let papersSemester = '1';
        let papersSubject = '__all__';
        let papersSearchQuery = '';

        let syllabusCache = [];
        let syllabusFaculty = 'BEL';
        let syllabusSemester = '1';
        let syllabusSubject = '__all__';
        let syllabusSearchQuery = '';

        let communityCache = [];
        let communitySearchQuery = '';

        function formatBytes(bytes) {
            if (!Number.isFinite(bytes) || bytes <= 0) return '0 B';
            const units = ['B', 'KB', 'MB', 'GB'];
            let i = 0;
            let n = bytes;
            while (n >= 1024 && i < units.length - 1) {
                n /= 1024;
                i++;
            }
            return `${n.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
        }

        function formatDate(iso) {
            if (!iso) return '';
            const d = new Date(iso);
            if (Number.isNaN(d.getTime())) return '';
            return d.toLocaleString();
        }

        async function fetchFiles(category) {
            const res = await fetch(`${API_BASE}/api/files/${category}`);
            if (!res.ok) throw new Error('Failed to load files');
            return res.json();
        }

        function makeCard({ id, title, metaLine, footer, externalUrl }) {
            const card = document.createElement('div');
            card.className = 'file-card';

            const header = document.createElement('div');
            header.className = 'file-card-header';

            const info = document.createElement('div');
            info.className = 'file-card-info';

            const h3 = document.createElement('h3');
            h3.textContent = title;

            const meta = document.createElement('p');
            meta.className = 'file-card-meta';
            meta.textContent = metaLine;

            info.appendChild(h3);
            info.appendChild(meta);

            const btn = document.createElement('button');
            btn.className = 'download-btn';
            if (externalUrl) {
                btn.textContent = '↗ Open';
                btn.addEventListener('click', () => window.open(externalUrl, '_blank', 'noopener'));
            } else {
                btn.textContent = '⬇ Download';
                btn.addEventListener('click', () => downloadFile(id));
            }

            header.appendChild(info);
            header.appendChild(btn);

            const foot = document.createElement('p');
            foot.className = 'file-card-footer';
            foot.textContent = footer;

            card.appendChild(header);
            card.appendChild(foot);
            return card;
        }

        function renderList(listId, emptyId, files, mapper) {
            const list = document.getElementById(listId);
            const empty = document.getElementById(emptyId);

            // Remove existing cards (keep empty-state node for toggling)
            list.querySelectorAll('.file-card').forEach(n => n.remove());

            if (!files || files.length === 0) {
                empty.style.display = 'block';
                return;
            }

            empty.style.display = 'none';
            files.forEach(f => list.appendChild(mapper(f)));
        }

        async function refreshAll() {
            try {
                const [notes, papers, syllabus] = await Promise.all([
                    fetchFiles('notes'),
                    fetchFiles('past-papers'),
                    fetchFiles('syllabus')
                ]);

                notesCache = Array.isArray(notes.files) ? notes.files : [];
                renderNotes();

                papersCache = Array.isArray(papers.files) ? papers.files : [];
                renderPapers();

                syllabusCache = Array.isArray(syllabus.files) ? syllabus.files : [];
                renderSyllabus();

                await refreshCommunity();
            } catch (err) {
                console.error(err);





            }
        }

        async function refreshCommunity() {
            const res = await fetch(`${API_BASE}/api/community/posts`);
            if (!res.ok) return;
            const data = await res.json().catch(() => ({}));
            communityCache = Array.isArray(data.posts) ? data.posts : [];
            renderCommunity();
        }

        function renderCommunity() {
            const list = document.getElementById('community-list');
            const empty = document.getElementById('community-empty');
            list.querySelectorAll('.file-card').forEach(n => n.remove());

            const q = (communitySearchQuery || '').toLowerCase();
            const posts = communityCache.filter(p => {
                if (!q) return true;
                const t = (p.title || '').toLowerCase();
                const b = (p.body || '').toLowerCase();
                const s = (p.meta?.subject || '').toLowerCase();
                const f = (p.meta?.faculty || '').toLowerCase();
                return t.includes(q) || b.includes(q) || s.includes(q) || f.includes(q);
            });

            if (posts.length === 0) {
                empty.style.display = 'block';
                return;
            }
            empty.style.display = 'none';

            posts.forEach(p => {
                const card = document.createElement('div');
                card.className = 'file-card';

                const header = document.createElement('div');
                header.className = 'file-card-header';

                const info = document.createElement('div');
                info.className = 'file-card-info';

                const h3 = document.createElement('h3');
                h3.textContent = p.title || 'Untitled';

                const meta = document.createElement('p');
                meta.className = 'file-card-meta';
                const fac = p.meta?.faculty || 'Any';
                const sem = p.meta?.semester || 'Any';
                const sub = p.meta?.subject || 'Any subject';
                meta.textContent = `Faculty: ${fac} | Semester: ${sem} | Subject: ${sub}`;

                info.appendChild(h3);
                info.appendChild(meta);

                const actions = document.createElement('div');
                actions.style.display = 'flex';
                actions.style.gap = '8px';
                actions.style.alignItems = 'center';

                const up = document.createElement('button');
                up.className = 'chip-btn';
                up.textContent = '▲';
                up.addEventListener('click', () => votePost(p.id, 'up'));

                const score = document.createElement('div');
                score.style.minWidth = '28px';
                score.style.textAlign = 'center';
                score.style.fontWeight = '800';
                score.textContent = `${p.score ?? 0}`;

                const down = document.createElement('button');
                down.className = 'chip-btn';
                down.textContent = '▼';
                down.addEventListener('click', () => votePost(p.id, 'down'));

                actions.appendChild(up);
                actions.appendChild(score);
                actions.appendChild(down);

                if (p.attachment) {
                    const dl = document.createElement('button');
                    dl.className = 'download-btn';
                    dl.textContent = '⬇ Download';
                    dl.addEventListener('click', () => {
                        window.location.href = `${API_BASE}/community/download/${encodeURIComponent(p.id)}`;
                    });
                    actions.appendChild(dl);
                }

                header.appendChild(info);
                header.appendChild(actions);

                const foot = document.createElement('p');
                foot.className = 'file-card-footer';
                const when = formatDate(p.created_at);
                const size = p.attachment?.size_bytes ? ` • ${formatBytes(p.attachment.size_bytes)}` : '';
                foot.textContent = `Posted ${when}${size}`;

                card.appendChild(header);
                if (p.body) {
                    const body = document.createElement('p');
                    body.style.margin = '10px 0 0';
                    body.style.color = '#666';
                    body.style.fontSize = '13px';
                    body.textContent = p.body;
                    card.appendChild(body);
                }
                card.appendChild(foot);
                list.appendChild(card);
            });
        }

        async function createPost(event) {
            event.preventDefault();
            try {
                const form = new FormData();
                const faculty = document.getElementById('community-faculty').value;
                const semester = document.getElementById('community-semester').value;
                const subject = document.getElementById('community-subject').value.trim();
                const title = document.getElementById('community-title').value.trim();
                const body = document.getElementById('community-body').value.trim();
                const file = document.getElementById('community-file').files[0];

                form.append('faculty', faculty);
                form.append('semester', semester);
                form.append('subject', subject);
                form.append('title', title);
                form.append('body', body);
                if (file) form.append('file', file);

                const res = await fetch(`${API_BASE}/api/community/posts`, { method: 'POST', body: form });
                const data = await res.json().catch(() => ({}));
                if (!res.ok) throw new Error(data?.error || 'Post failed');

                document.getElementById('community-form').reset();
                showSuccess('community-success', 'Posted to community!');
                await refreshCommunity();
            } catch (e) {
                showError('community-error', e.message || 'Post failed');
            }
        }

        async function votePost(id, direction) {
            try {
                const res = await fetch(`${API_BASE}/api/community/vote/${encodeURIComponent(id)}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ direction })
                });
                const data = await res.json().catch(() => ({}));
                if (!res.ok) throw new Error(data?.error || 'Vote failed');
                await refreshCommunity();
            } catch (e) {
                showError('community-error', e.message || 'Vote failed');
            }
        }

        function setActiveChips(selector, attr, value) {
            document.querySelectorAll(selector).forEach(btn => {
                if (btn.getAttribute(attr) === value) btn.classList.add('active');
                else btn.classList.remove('active');
            });
        }

        function selectFaculty(fac) {
            if (!FACULTIES.includes(fac)) return;
            selectedFaculty = fac;
            selectedSubject = '__all__';
            setActiveChips('#notes-faculty-row .chip-btn', 'data-faculty', fac);
            setActiveChips('#notes-subject-row .chip-btn', 'data-subject', '__all__');
            renderNotes();
        }

        function selectSemester(sem) {
            if (!SEMESTERS.includes(sem)) return;
            selectedSemester = sem;
            selectedSubject = '__all__';
            setActiveChips('#notes-semester-row .chip-btn', 'data-semester', sem);
            setActiveChips('#notes-subject-row .chip-btn', 'data-subject', '__all__');
            renderNotes();
        }

        function selectSubject(subj) {
            selectedSubject = subj;
            setActiveChips('#notes-subject-row .chip-btn', 'data-subject', subj);
            renderNotes();
        }

        function normalize(s) {
            return (s || '').toString().trim();
        }

        function subjectKey(s) {
            return normalize(s).toLowerCase();
        }

        function uniqueResourceKey(f) {
            const m = f?.meta || {};
            const code = normalize(m.code);
            const type = normalize(m.type);
            const fac = normalize(m.faculty);
            const sem = normalize(m.semester);
            const subj = normalize(m.subject);
            const original = normalize(f.original_name);
            const stored = normalize(f.stored_name);
            const external = normalize(f.external_url);
            return [
                normalize(f.category),
                fac,
                sem,
                subj,
                code,
                type,
                original,
                external,
                stored
            ].join('||');
        }

        function dedupeFiles(files) {
            const seen = new Set();
            const out = [];
            (files || []).forEach(f => {
                const k = uniqueResourceKey(f);
                if (seen.has(k)) return;
                seen.add(k);
                out.push(f);
            });
            return out;
        }

        function getPresetSubjects(faculty, semester) {
            const fac = SUBJECTS_BY_FAC_SEM?.[faculty];
            const list = fac?.[semester];
            return Array.isArray(list) ? list : null;
        }

        function buildSubjectButtons(files) {
            const container = document.getElementById('notes-subject-dynamic');
            container.innerHTML = '';

            const preset = getPresetSubjects(selectedFaculty, selectedSemester);
            const subjects = (preset || []).slice();

            if (!preset) {
                const subjectsMap = new Map();
                files.forEach(f => {
                    const sub = normalize(f.meta?.subject);
                    if (!sub) return;
                    const key = subjectKey(sub);
                    if (!subjectsMap.has(key)) subjectsMap.set(key, sub);
                });
                subjects.push(...Array.from(subjectsMap.values()));
                subjects.sort((a, b) => a.localeCompare(b));
            }

            subjects.forEach(sub => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'chip-btn';
                btn.setAttribute('data-subject', sub);
                btn.textContent = sub;
                btn.addEventListener('click', () => selectSubject(sub));
                container.appendChild(btn);
            });
        }

        function buildSubjectButtonsInto(containerId, files, onClick) {
            const container = document.getElementById(containerId);
            container.innerHTML = '';

            // Detect which navigator this belongs to by containerId
            let fac = null;
            let sem = null;
            if (containerId === 'papers-subject-dynamic') {
                fac = papersFaculty;
                sem = papersSemester;
            } else if (containerId === 'syllabus-subject-dynamic') {
                fac = syllabusFaculty;
                sem = syllabusSemester;
            }

            const preset = fac && sem ? getPresetSubjects(fac, sem) : null;
            const subjects = (preset || []).slice();

            if (!preset) {
                const subjectsMap = new Map();
                files.forEach(f => {
                    const sub = normalize(f.meta?.subject);
                    if (!sub) return;
                    const key = subjectKey(sub);
                    if (!subjectsMap.has(key)) subjectsMap.set(key, sub);
                });
                subjects.push(...Array.from(subjectsMap.values()));
                subjects.sort((a, b) => a.localeCompare(b));
            }

            subjects.forEach(sub => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'chip-btn';
                btn.setAttribute('data-subject', sub);
                btn.textContent = sub;
                btn.addEventListener('click', () => onClick(sub));
                container.appendChild(btn);
            });
        }

        function renderNotes() {
            // keep chip UI consistent (defaults)
            setActiveChips('#notes-faculty-row .chip-btn', 'data-faculty', selectedFaculty);
            setActiveChips('#notes-semester-row .chip-btn', 'data-semester', selectedSemester);
            setActiveChips('#notes-subject-row .chip-btn', 'data-subject', selectedSubject);

            const filteredByFacSem = dedupeFiles(notesCache.filter(f => {
                const fac = normalize(f.meta?.faculty);
                const sem = normalize(f.meta?.semester);
                return fac === selectedFaculty && sem === selectedSemester;
            }));

            buildSubjectButtons(filteredByFacSem);

            // After rebuilding buttons, re-apply active state (DOM changed)
            setActiveChips('#notes-subject-row .chip-btn', 'data-subject', selectedSubject);

            const q = (notesSearchQuery || '').toLowerCase();
            const files = dedupeFiles(filteredByFacSem.filter(f => {
                if (selectedSubject !== '__all__') {
                    const s = normalize(f.meta?.subject);
                    if (s !== selectedSubject) return false;
                }
                if (!q) return true;
                const subject = normalize(f.meta?.subject).toLowerCase();
                const topic = normalize(f.meta?.topic).toLowerCase();
                const original = normalize(f.original_name).toLowerCase();
                return subject.includes(q) || topic.includes(q) || original.includes(q);
            }));

            const subjectFiles = document.getElementById('notes-subject-files');
            subjectFiles.innerHTML = '';
            if (selectedSubject === '__all__') {
                // Show a grouped view by subject for this faculty+semester
                const bySubject = new Map();
                filteredByFacSem.forEach(f => {
                    const sub = normalize(f.meta?.subject) || 'Unknown subject';
                    if (!bySubject.has(sub)) bySubject.set(sub, []);
                    bySubject.get(sub).push(f);
                });
                Array.from(bySubject.keys()).sort((a, b) => a.localeCompare(b)).forEach(sub => {
                    const header = document.createElement('div');
                    header.style.margin = '10px 0 6px';
                    header.style.fontWeight = '700';
                    header.style.color = '#333';
                    header.textContent = sub;
                    subjectFiles.appendChild(header);
                    dedupeFiles(bySubject.get(sub)).forEach(f => {
                        const topic = f.meta?.topic || 'Notes';
                        const fac = f.meta?.faculty || '—';
                        const sem = f.meta?.semester || '—';
                        const title = `${sub} - ${topic}`;
                        const metaLine = `Faculty: ${fac} | Semester: ${sem} | Original: ${f.original_name}`;
                        const footer = `📄 ${formatBytes(f.size_bytes)} • Uploaded ${formatDate(f.uploaded_at)}`;
                        subjectFiles.appendChild(makeCard({ id: f.id, title, metaLine, footer, externalUrl: f.external_url }));
                    });
                });
            } else {
                // Show files directly under the chosen subject
                if (files.length === 0) {
                    const empty = document.createElement('div');
                    empty.className = 'empty-state';
                    empty.innerHTML = '<div class="empty-state-icon">📂</div><div>No files uploaded for this subject yet.</div>';
                    subjectFiles.appendChild(empty);
                } else {
                    files.forEach(f => {
                        const subject = f.meta?.subject || 'Unknown subject';
                        const topic = f.meta?.topic || 'Notes';
                        const fac = f.meta?.faculty || '—';
                        const sem = f.meta?.semester || '—';
                        const title = `${subject} - ${topic}`;
                        const metaLine = `Faculty: ${fac} | Semester: ${sem} | Original: ${f.original_name}`;
                        const footer = `📄 ${formatBytes(f.size_bytes)} • Uploaded ${formatDate(f.uploaded_at)}`;
                        subjectFiles.appendChild(makeCard({ id: f.id, title, metaLine, footer, externalUrl: f.external_url }));
                    });
                }
            }

            // Bottom list is hidden; subjectFiles is the main renderer now.
        }

        function selectPapersFaculty(fac) {
            if (!FACULTIES.includes(fac)) return;
            papersFaculty = fac;
            papersSubject = '__all__';
            setActiveChips('#papers-faculty-row .chip-btn', 'data-faculty', fac);
            setActiveChips('#papers-subject-row .chip-btn', 'data-subject', '__all__');
            renderPapers();
        }

        function selectPapersSemester(sem) {
            if (!SEMESTERS.includes(sem)) return;
            papersSemester = sem;
            papersSubject = '__all__';
            setActiveChips('#papers-semester-row .chip-btn', 'data-semester', sem);
            setActiveChips('#papers-subject-row .chip-btn', 'data-subject', '__all__');
            renderPapers();
        }

        function selectPapersSubject(subj) {
            papersSubject = subj;
            setActiveChips('#papers-subject-row .chip-btn', 'data-subject', subj);
            renderPapers();
        }

        function renderPapers() {
            setActiveChips('#papers-faculty-row .chip-btn', 'data-faculty', papersFaculty);
            setActiveChips('#papers-semester-row .chip-btn', 'data-semester', papersSemester);
            setActiveChips('#papers-subject-row .chip-btn', 'data-subject', papersSubject);

            const base = dedupeFiles(papersCache.filter(f => {
                const fac = normalize(f.meta?.faculty);
                const sem = normalize(f.meta?.semester);
                return fac === papersFaculty && sem === papersSemester;
            }));

            buildSubjectButtonsInto('papers-subject-dynamic', base, (s) => selectPapersSubject(s));
            setActiveChips('#papers-subject-row .chip-btn', 'data-subject', papersSubject);

            const q = (papersSearchQuery || '').toLowerCase();
            const filtered = dedupeFiles(base.filter(f => {
                if (papersSubject !== '__all__' && normalize(f.meta?.subject) !== papersSubject) return false;
                if (!q) return true;
                const subject = normalize(f.meta?.subject).toLowerCase();
                const year = normalize(f.meta?.year).toLowerCase();
                const type = normalize(f.meta?.type).toLowerCase();
                const original = normalize(f.original_name).toLowerCase();
                return subject.includes(q) || year.includes(q) || type.includes(q) || original.includes(q);
            }));

            const subjectFiles = document.getElementById('papers-subject-files');
            subjectFiles.innerHTML = '';
            const toShow = filtered;
            if (papersSubject === '__all__') {
                // grouped by subject
                const bySubject = new Map();
                base.forEach(f => {
                    const sub = normalize(f.meta?.subject) || 'Unknown subject';
                    if (!bySubject.has(sub)) bySubject.set(sub, []);
                    bySubject.get(sub).push(f);
                });
                Array.from(bySubject.keys()).sort((a, b) => a.localeCompare(b)).forEach(sub => {
                    const header = document.createElement('div');
                    header.style.margin = '10px 0 6px';
                    header.style.fontWeight = '700';
                    header.style.color = '#333';
                    header.textContent = sub;
                    subjectFiles.appendChild(header);
                    dedupeFiles(bySubject.get(sub)).forEach(f => {
                        const year = f.meta?.year || '—';
                        const type = f.meta?.type || 'Exam';
                        const fac = f.meta?.faculty || '—';
                        const sem = f.meta?.semester || '—';
                        const title = `${sub} - ${type} ${year}`;
                        const metaLine = `Faculty: ${fac} | Semester: ${sem} | Year: ${year} | Type: ${type} | Original: ${f.original_name}`;
                        const footer = `📄 ${formatBytes(f.size_bytes)} • Uploaded ${formatDate(f.uploaded_at)}`;
                        subjectFiles.appendChild(makeCard({ id: f.id, title, metaLine, footer, externalUrl: f.external_url }));
                    });
                });
            } else {
                if (toShow.length === 0) {
                    const empty = document.createElement('div');
                    empty.className = 'empty-state';
                    empty.innerHTML = '<div class="empty-state-icon">📂</div><div>No papers uploaded for this subject yet.</div>';
                    subjectFiles.appendChild(empty);
                } else {
                    dedupeFiles(toShow).forEach(f => {
                        const subject = f.meta?.subject || 'Unknown subject';
                        const year = f.meta?.year || '—';
                        const type = f.meta?.type || 'Exam';
                        const fac = f.meta?.faculty || '—';
                        const sem = f.meta?.semester || '—';
                        const title = `${subject} - ${type} ${year}`;
                        const metaLine = `Faculty: ${fac} | Semester: ${sem} | Year: ${year} | Type: ${type} | Original: ${f.original_name}`;
                        const footer = `📄 ${formatBytes(f.size_bytes)} • Uploaded ${formatDate(f.uploaded_at)}`;
                        subjectFiles.appendChild(makeCard({ id: f.id, title, metaLine, footer, externalUrl: f.external_url }));
                    });
                }
            }

            // Bottom list is hidden; subjectFiles is the main renderer now.
        }

        function selectSyllabusFaculty(fac) {
            if (!FACULTIES.includes(fac)) return;
            syllabusFaculty = fac;
            syllabusSubject = '__all__';
            setActiveChips('#syllabus-faculty-row .chip-btn', 'data-faculty', fac);
            setActiveChips('#syllabus-subject-row .chip-btn', 'data-subject', '__all__');
            renderSyllabus();
        }

        function selectSyllabusSemester(sem) {
            if (!SEMESTERS.includes(sem)) return;
            syllabusSemester = sem;
            syllabusSubject = '__all__';
            setActiveChips('#syllabus-semester-row .chip-btn', 'data-semester', sem);
            setActiveChips('#syllabus-subject-row .chip-btn', 'data-subject', '__all__');
            renderSyllabus();
        }

        function selectSyllabusSubject(subj) {
            syllabusSubject = subj;
            setActiveChips('#syllabus-subject-row .chip-btn', 'data-subject', subj);
            renderSyllabus();
        }

        function renderSyllabus() {
            setActiveChips('#syllabus-faculty-row .chip-btn', 'data-faculty', syllabusFaculty);
            setActiveChips('#syllabus-semester-row .chip-btn', 'data-semester', syllabusSemester);
            setActiveChips('#syllabus-subject-row .chip-btn', 'data-subject', syllabusSubject);

            const base = dedupeFiles(syllabusCache.filter(f => {
                const fac = normalize(f.meta?.faculty);
                const sem = normalize(f.meta?.semester);
                return fac === syllabusFaculty && sem === syllabusSemester;
            }));

            buildSubjectButtonsInto('syllabus-subject-dynamic', base, (s) => selectSyllabusSubject(s));
            setActiveChips('#syllabus-subject-row .chip-btn', 'data-subject', syllabusSubject);

            const q = (syllabusSearchQuery || '').toLowerCase();
            const filtered = dedupeFiles(base.filter(f => {
                if (syllabusSubject !== '__all__' && normalize(f.meta?.subject) !== syllabusSubject) return false;
                if (!q) return true;
                const subject = normalize(f.meta?.subject).toLowerCase();
                const code = normalize(f.meta?.code).toLowerCase();
                const instructor = normalize(f.meta?.instructor).toLowerCase();
                const original = normalize(f.original_name).toLowerCase();
                return subject.includes(q) || code.includes(q) || instructor.includes(q) || original.includes(q);
            }));

            const subjectFiles = document.getElementById('syllabus-subject-files');
            subjectFiles.innerHTML = '';

            if (syllabusSubject === '__all__') {
                const bySubject = new Map();
                base.forEach(f => {
                    const sub = normalize(f.meta?.subject) || 'Unknown course';
                    if (!bySubject.has(sub)) bySubject.set(sub, []);
                    bySubject.get(sub).push(f);
                });
                Array.from(bySubject.keys()).sort((a, b) => a.localeCompare(b)).forEach(sub => {
                    const header = document.createElement('div');
                    header.style.margin = '10px 0 6px';
                    header.style.fontWeight = '700';
                    header.style.color = '#333';
                    header.textContent = sub;
                    subjectFiles.appendChild(header);
                    dedupeFiles(bySubject.get(sub)).forEach(f => {
                        const code = f.meta?.code || '—';
                        const instructor = f.meta?.instructor || '—';
                        const fac = f.meta?.faculty || '—';
                        const sem = f.meta?.semester || '—';
                        const title = `${sub} (${code})`;
                        const metaLine = `Faculty: ${fac} | Semester: ${sem} | Instructor: ${instructor} | Original: ${f.original_name}`;
                        const footer = `📄 ${formatBytes(f.size_bytes)} • Uploaded ${formatDate(f.uploaded_at)}`;
                        subjectFiles.appendChild(makeCard({ id: f.id, title, metaLine, footer, externalUrl: f.external_url }));
                    });
                });
            } else {
                if (filtered.length === 0) {
                    const empty = document.createElement('div');
                    empty.className = 'empty-state';
                    empty.innerHTML = '<div class="empty-state-icon">📂</div><div>No syllabus uploaded for this subject yet.</div>';
                    subjectFiles.appendChild(empty);
                } else {
                    filtered.forEach(f => {
                        const subject = f.meta?.subject || 'Unknown course';
                        const code = f.meta?.code || '—';
                        const instructor = f.meta?.instructor || '—';
                        const fac = f.meta?.faculty || '—';
                        const sem = f.meta?.semester || '—';
                        const title = `${subject} (${code})`;
                        const metaLine = `Faculty: ${fac} | Semester: ${sem} | Instructor: ${instructor} | Original: ${f.original_name}`;
                        const footer = `📄 ${formatBytes(f.size_bytes)} • Uploaded ${formatDate(f.uploaded_at)}`;
                        subjectFiles.appendChild(makeCard({ id: f.id, title, metaLine, footer, externalUrl: f.external_url }));
                    });
                }
            }

            // Bottom list is hidden; subjectFiles is the main renderer now.
        }

        // Download File
        function downloadFile(fileId) {
            window.location.href = `${API_BASE}/download/${encodeURIComponent(fileId)}`;
        }

        // Show success message
        function showSuccess(elementId, message) {
            const element = document.getElementById(elementId);
            element.textContent = message;
            element.classList.add('show');
            
            setTimeout(() => {
                element.classList.remove('show');
            }, 4000);
        }

        // Show error message
        function showError(elementId, message) {
            const element = document.getElementById(elementId);
            element.textContent = message;
            element.classList.add('show');
            
            setTimeout(() => {
                element.classList.remove('show');
            }, 4000);
        }

        // Search functionality
        document.getElementById('notes-search').addEventListener('input', (e) => {
            notesSearchQuery = e.target.value || '';
            renderNotes();
        });

        document.getElementById('papers-search').addEventListener('input', (e) => {
            papersSearchQuery = e.target.value || '';
            renderPapers();
        });

        document.getElementById('syllabus-search').addEventListener('input', (e) => {
            syllabusSearchQuery = e.target.value || '';
            renderSyllabus();
        });

        document.getElementById('community-search').addEventListener('input', (e) => {
            communitySearchQuery = e.target.value || '';
            renderCommunity();
        });

        function filterCards(listId, query) {
            const list = document.getElementById(listId);
            const cards = list.querySelectorAll('.file-card');
            
            cards.forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const meta = card.querySelector('.file-card-meta').textContent.toLowerCase();
                
                if (title.includes(query) || meta.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        document.addEventListener('DOMContentLoaded', () => {
            // defaults for the new notes navigator
            selectFaculty(selectedFaculty);
            selectSemester(selectedSemester);

            // defaults for other navigators
            selectPapersFaculty(papersFaculty);
            selectPapersSemester(papersSemester);
            selectSyllabusFaculty(syllabusFaculty);
            selectSyllabusSemester(syllabusSemester);
            refreshAll();
        });