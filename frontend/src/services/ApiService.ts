/**
 * Serwis do komunikacji z API backendu
 */
import axios from 'axios';

// Bazowy URL API
const API_BASE_URL = 'http://localhost:8000';

// Interfejsy dla danych
interface SkillMatch {
  cv_skill: string;
  job_skill: string;
  similarity_score: number;
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

interface ApiResponse {
  status: string;
  message: string;
  files: {
    cv: string;
    job_description: string;
  };
  analysis: AnalysisResult;
  cv_data?: {
    full_text: string;
    [key: string]: any;
  };
  job_data?: {
    full_text: string;
    [key: string]: any;
  };
}

/**
 * Klasa serwisu API
 */
class ApiService {
  /**
   * Wysyła pliki CV i ogłoszenia do analizy
   * @param cvFile Plik CV
   * @param jobDescFile Plik ogłoszenia o pracę
   * @returns Wynik analizy
   */
  async analyzeFiles(cvFile: File, jobDescFile: File): Promise<ApiResponse> {
    try {
      const formData = new FormData();
      formData.append('cv_file', cvFile);
      formData.append('job_description_file', jobDescFile);
      
      const response = await axios.post<ApiResponse>(`${API_BASE_URL}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          throw new Error(`Błąd serwera: ${error.response.status} - ${error.response.data.detail || 'Nieznany błąd'}`);
        } else if (error.request) {
          throw new Error('Brak odpowiedzi z serwera. Sprawdź połączenie internetowe lub czy serwer jest uruchomiony.');
        }
      }
      throw new Error('Wystąpił nieoczekiwany błąd podczas analizy plików.');
    }
  }
  
  /**
   * Sprawdza status serwera
   * @returns Status serwera
   */
  async checkHealth(): Promise<{ status: string, timestamp: string }> {
    try {
      const response = await axios.get<{ status: string, timestamp: string }>(`${API_BASE_URL}/health`);
      return response.data;
    } catch (error) {
      throw new Error('Nie można połączyć się z serwerem API.');
    }
  }
}

// Eksport instancji serwisu
export default new ApiService();
