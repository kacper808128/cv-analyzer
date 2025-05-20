/**
 * Komponent do wyświetlania przykładowych danych testowych
 * Używany do walidacji frontendu bez konieczności łączenia z backendem
 */
import React, { useState } from 'react';
import ResultsView from '../components/ResultsView';
import '../styles/MockDataTester.css';

// Przykładowe dane do testów
const mockAnalysisResult = {
  relevance_score: 0.75,
  section_scores: {
    skills: 0.8,
    experience: 0.7,
    education: 0.6,
    full_text: 0.65
  },
  skill_matches: [
    { cv_skill: "JavaScript", job_skill: "JavaScript", similarity_score: 1.0 },
    { cv_skill: "TypeScript", job_skill: "TypeScript", similarity_score: 1.0 },
    { cv_skill: "React", job_skill: "React", similarity_score: 1.0 },
    { cv_skill: "Node.js", job_skill: "Node.js", similarity_score: 1.0 },
    { cv_skill: "Python", job_skill: "Python", similarity_score: 1.0 },
    { cv_skill: "SQL", job_skill: "SQL", similarity_score: 1.0 },
    { cv_skill: "Docker", job_skill: "Docker", similarity_score: 1.0 },
    { cv_skill: "Git", job_skill: "CI/CD", similarity_score: 0.6 }
  ],
  highlighted_keywords: [
    "JavaScript", "TypeScript", "React", "Node.js", "Python", 
    "SQL", "Docker", "Git", "API", "frontend", "backend"
  ]
};

const mockCvText = `Jan Kowalski
Senior Full-Stack Developer

Kontakt:
Email: jan.kowalski@example.com
Telefon: +48 123 456 789
LinkedIn: linkedin.com/in/jankowalski

Podsumowanie zawodowe:
Doświadczony Full-Stack Developer z ponad 5-letnim doświadczeniem w tworzeniu aplikacji webowych. Specjalizuję się w technologiach JavaScript/TypeScript, React, Node.js oraz Python. Posiadam umiejętność pracy w środowisku Agile i doświadczenie w prowadzeniu małych zespołów programistycznych.

Doświadczenie zawodowe:

Senior Full-Stack Developer
Tech Solutions Sp. z o.o.
2020 - obecnie
- Rozwój aplikacji webowych z wykorzystaniem React i Node.js
- Implementacja architektury mikroserwisowej
- Optymalizacja wydajności aplikacji
- Code review i mentoring juniorów
- Wdrażanie praktyk CI/CD

Full-Stack Developer
WebDev Company
2018 - 2020
- Implementacja funkcjonalności front-end i back-end
- Integracja z zewnętrznymi API
- Rozwój aplikacji mobilnych z React Native
- Utrzymanie i rozwój baz danych SQL i NoSQL

Junior Developer
StartupTech
2016 - 2018
- Rozwój interfejsów użytkownika z wykorzystaniem React
- Implementacja REST API z wykorzystaniem Express.js
- Testowanie aplikacji

Wykształcenie:

Magister Informatyki
Politechnika Warszawska
2016 - 2018

Inżynier Informatyki
Politechnika Warszawska
2012 - 2016

Umiejętności techniczne:
- Języki programowania: JavaScript, TypeScript, Python, HTML, CSS
- Frontend: React, Redux, Angular, Vue.js
- Backend: Node.js, Express, FastAPI, Django
- Bazy danych: PostgreSQL, MongoDB, Redis
- DevOps: Docker, Kubernetes, AWS, CI/CD
- Narzędzia: Git, Jira, Confluence, Webpack
- Metodologie: Agile, Scrum, TDD`;

const mockJobText = `Senior Full-Stack Developer
Innowacyjne Rozwiązania IT

O firmie:
Innowacyjne Rozwiązania IT to dynamicznie rozwijająca się firma z branży IT, specjalizująca się w tworzeniu nowoczesnych aplikacji webowych i mobilnych dla klientów z różnych sektorów. Nasz zespół składa się z doświadczonych specjalistów, którzy cenią sobie profesjonalizm, kreatywność i innowacyjne podejście do rozwiązywania problemów.

Opis stanowiska:
Poszukujemy doświadczonego Senior Full-Stack Developera, który dołączy do naszego zespołu i weźmie udział w rozwoju zaawansowanych aplikacji webowych. Osoba na tym stanowisku będzie odpowiedzialna za projektowanie, implementację i utrzymanie aplikacji, współpracę z zespołem UX/UI oraz udział w podejmowaniu kluczowych decyzji technologicznych.

Obowiązki:
- Rozwój aplikacji webowych z wykorzystaniem nowoczesnych technologii
- Implementacja nowych funkcjonalności zarówno po stronie front-end, jak i back-end
- Optymalizacja wydajności istniejących rozwiązań
- Code review i zapewnienie wysokiej jakości kodu
- Współpraca z zespołem UX/UI przy projektowaniu interfejsów użytkownika
- Udział w planowaniu sprintów i estymacji zadań
- Mentoring dla mniej doświadczonych członków zespołu

Wymagania:
- Minimum 3 lata doświadczenia w rozwoju aplikacji webowych
- Bardzo dobra znajomość JavaScript/TypeScript, React i Node.js
- Doświadczenie z bazami danych SQL (PostgreSQL) i NoSQL (MongoDB)
- Znajomość konteneryzacji (Docker) i orkiestracji (Kubernetes)
- Doświadczenie w pracy z systemami kontroli wersji (Git)
- Znajomość praktyk CI/CD
- Umiejętność pracy w metodologii Agile/Scrum
- Wykształcenie wyższe techniczne (informatyka lub pokrewne)
- Bardzo dobra znajomość języka angielskiego

Umiejętności techniczne:
- JavaScript
- TypeScript
- React
- Node.js
- Python
- SQL
- NoSQL
- Docker
- Kubernetes
- CI/CD
- Git
- REST API
- Agile/Scrum`;

const MockDataTester: React.FC = () => {
  const [showResults, setShowResults] = useState(false);

  return (
    <div className="mock-data-tester">
      {!showResults ? (
        <div className="mock-controls">
          <h2>Tester przykładowych danych</h2>
          <p>
            Ten komponent pozwala na testowanie widoku wyników bez konieczności łączenia z backendem.
            Kliknij przycisk poniżej, aby wyświetlić przykładowe wyniki analizy.
          </p>
          <button 
            className="mock-button"
            onClick={() => setShowResults(true)}
          >
            Pokaż przykładowe wyniki
          </button>
        </div>
      ) : (
        <ResultsView 
          result={mockAnalysisResult}
          cvText={mockCvText}
          jobText={mockJobText}
          onReset={() => setShowResults(false)}
        />
      )}
    </div>
  );
};

export default MockDataTester;
