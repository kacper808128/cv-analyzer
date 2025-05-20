import React from 'react';
import '../styles/ResultsView.css';

// Interfejsy dla danych wynikowych
interface SkillMatch {
  cv_skill: string;
  job_skill: string;
  similarity_score: number;
}

interface SectionScore {
  section_name: string;
  score: number;
  weight: number;
}

interface AnalysisResult {
  relevance_score: number;
  section_scores: {
    skills: number;
    experience: number;
    education: number;
    full_text: number;
  };
  skill_matches: SkillMatch[];
  highlighted_keywords: string[];
}

interface ResultsViewProps {
  result: AnalysisResult;
  cvText: string;
  jobText: string;
  onReset: () => void;
}

const ResultsView: React.FC<ResultsViewProps> = ({ result, cvText, jobText, onReset }) => {
  // Funkcja do formatowania procentów
  const formatPercent = (value: number): string => {
    return `${Math.round(value * 100)}%`;
  };

  // Funkcja do określania klasy CSS na podstawie wyniku
  const getScoreClass = (score: number): string => {
    if (score >= 0.8) return 'score-high';
    if (score >= 0.6) return 'score-medium';
    return 'score-low';
  };

  // Funkcja do podświetlania słów kluczowych w tekście
  const highlightKeywords = (text: string, keywords: string[]): JSX.Element => {
    if (!keywords.length) return <>{text}</>;

    const regex = new RegExp(`(${keywords.join('|')})`, 'gi');
    const parts = text.split(regex);

    return (
      <>
        {parts.map((part, i) => {
          const isKeyword = keywords.some(keyword => 
            part.toLowerCase() === keyword.toLowerCase()
          );
          return isKeyword ? 
            <span key={i} className="highlighted-keyword">{part}</span> : 
            <span key={i}>{part}</span>;
        })}
      </>
    );
  };

  return (
    <div className="results-container">
      <h2>Wyniki analizy dopasowania CV</h2>
      
      {/* Główny wynik */}
      <div className="main-score-container">
        <div className={`main-score ${getScoreClass(result.relevance_score)}`}>
          <div className="score-value">{formatPercent(result.relevance_score)}</div>
          <div className="score-label">Dopasowanie</div>
        </div>
      </div>

      {/* Wyniki sekcji */}
      <div className="section-scores">
        <h3>Wyniki według sekcji</h3>
        <div className="score-bars">
          <div className="score-bar-item">
            <div className="score-bar-label">Umiejętności</div>
            <div className="score-bar-container">
              <div 
                className={`score-bar ${getScoreClass(result.section_scores.skills)}`}
                style={{ width: formatPercent(result.section_scores.skills) }}
              ></div>
            </div>
            <div className="score-bar-value">{formatPercent(result.section_scores.skills)}</div>
          </div>
          
          <div className="score-bar-item">
            <div className="score-bar-label">Doświadczenie</div>
            <div className="score-bar-container">
              <div 
                className={`score-bar ${getScoreClass(result.section_scores.experience)}`}
                style={{ width: formatPercent(result.section_scores.experience) }}
              ></div>
            </div>
            <div className="score-bar-value">{formatPercent(result.section_scores.experience)}</div>
          </div>
          
          <div className="score-bar-item">
            <div className="score-bar-label">Wykształcenie</div>
            <div className="score-bar-container">
              <div 
                className={`score-bar ${getScoreClass(result.section_scores.education)}`}
                style={{ width: formatPercent(result.section_scores.education) }}
              ></div>
            </div>
            <div className="score-bar-value">{formatPercent(result.section_scores.education)}</div>
          </div>
        </div>
      </div>

      {/* Dopasowanie umiejętności */}
      <div className="skill-matches">
        <h3>Dopasowanie umiejętności</h3>
        <div className="skills-table-container">
          <table className="skills-table">
            <thead>
              <tr>
                <th>Umiejętność z CV</th>
                <th>Umiejętność z ogłoszenia</th>
                <th>Dopasowanie</th>
              </tr>
            </thead>
            <tbody>
              {result.skill_matches.map((match, index) => (
                <tr key={index}>
                  <td>{match.cv_skill}</td>
                  <td>{match.job_skill}</td>
                  <td>
                    <div className="match-score-container">
                      <div 
                        className={`match-score ${getScoreClass(match.similarity_score)}`}
                        style={{ width: formatPercent(match.similarity_score) }}
                      ></div>
                      <span className="match-score-value">{formatPercent(match.similarity_score)}</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Podgląd dokumentów */}
      <div className="documents-preview">
        <h3>Podgląd dokumentów z podświetlonymi słowami kluczowymi</h3>
        <div className="documents-container">
          <div className="document-preview">
            <h4>CV</h4>
            <div className="document-content">
              {highlightKeywords(cvText, result.highlighted_keywords)}
            </div>
          </div>
          
          <div className="document-preview">
            <h4>Ogłoszenie o pracę</h4>
            <div className="document-content">
              {highlightKeywords(jobText, result.highlighted_keywords)}
            </div>
          </div>
        </div>
      </div>

      {/* Przycisk do nowej analizy */}
      <div className="action-buttons">
        <button className="reset-button" onClick={onReset}>
          Rozpocznij nową analizę
        </button>
      </div>
    </div>
  );
};

export default ResultsView;
