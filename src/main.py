import sys
from src.rag.rag_pipeline import create_and_run_graph

def main():
    """Main entry point for the interactive RAG application."""
    while True:
        source = input("Enter URL or local path (or type 'exit' to quit): ")
        if source.lower() == 'exit':
            break

        try:
            while True:
                question = input("Enter your question (or type 'new' to load new source, 'exit' to quit): ")
                if question.lower() == 'exit':
                    return
                if question.lower() == 'new':
                    break

                answer = create_and_run_graph(source, question)
                print("Answer:", answer)
                print("-" * 40)

        except Exception as e:
            print(f"An error occurred: {e}")
            print("-" * 40)

if __name__ == "__main__":
    main()