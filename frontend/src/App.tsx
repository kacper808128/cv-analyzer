import React, { useState } from 'react';
import './App.css';
import FileUploadForm from './components/FileUploadForm';
import ResultsView from './components/ResultsView';

// Interfejs dla danych wynikowych
interface AnalysisResult {
  relevance_score: number;
  section_scores: {
    skills: number;
    experience: number;
    education: number;
    full_text: number;
  };
  skill_matches: Array<{
    cv_skill: string;
    job_skill: string;
    similarity_score: number;
  }>;
  highlighted_keywords: string[];
}

function App() {
  // Stan aplikacji
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [cvText, setCvText] = useState<string>('');
  const [jobText, setJobText] = useState<string>('');

  // Funkcja do obsługi przesyłania plików
  const handleSubmit = async (cvFile: File, jobDescFile: File) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Tworzenie formularza do przesłania
      const formData = new FormData();
      formData.append('cv_file', cvFile);
      formData.append('job_description_file', jobDescFile);
      
      // Przesłanie plików do API
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Błąd serwera: ${response.status}`);
      }
      
      // Przetworzenie odpowiedzi
      const data = await response.json();
      
      // Ustawienie wyniku analizy
      setResult(data.analysis);
      
      // Ustawienie tekstów dokumentów (w rzeczywistej aplikacji byłyby pobierane z odpowiedzi API)
      setCvText(data.cv_data?.full_text || 'Tekst CV nie jest dostępny');
      setJobText(data.job_data?.full_text || 'Tekst ogłoszenia nie jest dostępny');
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Wystąpił nieznany błąd');
      console.error('Błąd podczas analizy:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Funkcja do resetowania stanu aplikacji
  const handleReset = () => {
    setResult(null);
    setCvText('');
    setJobText('');
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>CV Analyzer</h1>
        <p>Analiza CV pod kątem zgodności z ogłoszeniem o pracę</p>
      </header>
      
      <main className="app-content">
        {error && (
          <div className="error-container">
            <p className="error-message">{error}</p>
            <button onClick={() => setError(null)} className="error-dismiss">
              Zamknij
            </button>
          </div>
        )}
        
        {!result ? (
          <FileUploadForm onSubmit={handleSubmit} isLoading={isLoading} />
        ) : (
          <ResultsView 
            result={result} 
            cvText={cvText} 
            jobText={jobText} 
            onReset={handleReset} 
          />
        )}
      </main>
      
      <footer className="app-footer">
        <p>&copy; 2025 CV Analyzer - Analiza CV pod kątem zgodności z ogłoszeniem o pracę</p>
      </footer>
    </div>
  );
}

export default App;
