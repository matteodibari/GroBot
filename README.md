# GroBot, a RAG-based Chatbot

An informative and educational chatbot specifically designed to provide comprehensive knowledge about mangroves - their ecological significance, environmental benefits, and global importance. This specialized chatbot serves as an interactive learning tool to educate users about mangrove ecosystems, their role in climate change mitigation, biodiversity conservation, and coastal protection.

## 🌟 Features

- **Advanced RAG Pipeline**
  - Document chunking and embedding using Cohere embed v3
  - Semantic search with cosine similarity
  - Advanced reranking using Cohere rerank v3.5
  - Context-aware response generation

- **Modern Tech Stack**
  - Backend: FastAPI + Python
  - Frontend: Next.js + ShadCN UI
  - Clean, responsive chat interface
  - Real-time interaction

- **Production-Ready Architecture**
  - Modular and extensible design
  - Error handling and retry mechanisms
  - Environment-based configuration
  - Type safety with TypeScript and Python type hints

## 📚 Educational Content Focus

The chatbot provides detailed information on various aspects of mangroves:

- **Ecosystem Services**: Understanding how mangroves protect coastlines, support fisheries, and maintain water quality
- **Biodiversity**: Learning about the unique species that inhabit mangrove ecosystems
- **Climate Change**: Exploring mangroves' role in carbon sequestration and climate regulation
- **Conservation**: Information about mangrove restoration efforts and sustainable management practices
- **Global Impact**: Understanding the worldwide distribution and importance of mangrove forests

## 📖 Data Sources

The chatbot's knowledge base is built upon two key scientific papers that provide comprehensive coverage of mangrove ecosystems:

1. Feller, I. C., Lovelock, C. E., Berger, U., McKee, K. L., Joye, S. B., & Ball, M. C. (2010). Biocomplexity in Mangrove Ecosystems. *Annual Review of Marine Science*, 2, 395-417. https://doi.org/10.1146/annurev.marine.010908.163809
   - This paper provides a comprehensive review of the complex biological and ecological interactions within mangrove ecosystems.

2. Lee, S. Y. (1995). Mangrove outwelling: a review. *Hydrobiologia*, 295, 203-212.
   - This foundational study focuses on the role of mangroves in nutrient cycling and their contribution to adjacent ecosystems.

The selection of these two documents was carefully made to:
- Provide high-quality, peer-reviewed scientific information
- Cover complementary aspects of mangrove ecosystems (biological complexity and nutrient dynamics)
- Stay within the token limits of the Cohere API while maintaining comprehensive coverage

Note: The `purple_elephant.pdf` file in the data directory is used solely for testing the RAG pipeline functionality and does not contain mangrove-related content.

These documents are processed and indexed to provide accurate, science-based responses to user queries.

## Technical Stack

### Backend
- Python 3.8+
- FastAPI
- Cohere API (embeddings, reranking, chat)
- PDF processing capabilities
- Async/await for optimal performance

### Frontend
- Next.js 13+
- TypeScript
- ShadCN UI components
- Zustand for state management
- Tailwind CSS for styling

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Cohere API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/longevai-chatbot.git
cd longevai-chatbot
```

2. Set up the backend:
```bash
cd mangrove_chatbot/backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Set up the frontend:
```bash
cd ../frontend
npm install
```

### Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn app.main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Open your browser and navigate to `http://localhost:3000`

## 📁 Project Structure 

mangrove_chatbot/
├── backend/
│ ├── app/
│ │ ├── api.py # FastAPI routes
│ │ ├── rag.py # RAG pipeline implementation
│ │ ├── models.py # Data models
│ │ └── config.py # Configuration
│ ├── data/ # Document storage
│ └── requirements.txt # Python dependencies
│
└── frontend/
├── src/
│ ├── app/ # Next.js app directory
│ ├── components/ # React components
│ └── store/ # State management
├── package.json
└── tailwind.config.js


## 🔧 Configuration

### Backend Configuration
Create a `.env` file in the backend directory with:
```env
COHERE_API_KEY=your_api_key_here
```

### Frontend Configuration
Environment variables can be set in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Matteo Di Bari**

## 🙏 Acknowledgments

- [Cohere](https://cohere.ai/) for their powerful AI models
- [LongevAI](https://www.longev.ai/) for the project opportunity
- [ShadCN UI](https://ui.shadcn.com/) for the beautiful components
