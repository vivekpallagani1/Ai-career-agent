import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async register(email: string, password: string, name: string) {
    const response = await this.client.post('/auth/register', {
      email,
      password,
      name,
    });
    return response.data;
  }

  async login(email: string, password: string) {
    const response = await this.client.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  }

  async getJobs(limit = 20, offset = 0) {
    const response = await this.client.get('/jobs/', {
      params: { limit, offset },
    });
    return response.data;
  }

  async getJob(jobId: number) {
    const response = await this.client.get(`/jobs/${jobId}`);
    return response.data;
  }

  async searchJobs(title?: string, company?: string, location?: string) {
    const response = await this.client.get('/jobs/search', {
      params: { title, company, location },
    });
    return response.data;
  }

  async calculateJobMatch(jobId: number) {
    const response = await this.client.post(`/jobs/${jobId}/match`);
    return response.data;
  }

  async getProfile(profileId: number) {
    const response = await this.client.get(`/profiles/${profileId}`);
    return response.data;
  }

  async createProfile(data: Record<string, unknown>) {
    const response = await this.client.post('/profiles/', data);
    return response.data;
  }
}

export default new ApiClient();
