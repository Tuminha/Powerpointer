import { PineconeClient } from "@pinecone-database/pinecone";
import { VectorDBQAChain } from "langchain/chains";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { OpenAI } from "langchain/llms/openai";
import { PineconeStore } from "langchain/vectorstores/pinecone";

async function main() {
  try {
    const input = "What are the latest publications about socket shield?";  // Replace this with your question

    const client = new PineconeClient();
    await client.init({
      apiKey: process.env.PINECONE_API_KEY,
      environment: process.env.PINECONE_ENVIRONMENT,
    });

    const pineconeIndex = client.Index(process.env.PINECONE_INDEX);

    const vectorStore = await PineconeStore.fromExistingIndex(
      new OpenAIEmbeddings(),
      { pineconeIndex }
    );

    const model = new OpenAI();

    const chain = VectorDBQAChain.fromLLM(model, vectorStore, { k: 1, returnSourceDocuments: true });

    const response = await chain.call( { query: input });

    console.log(response);  // Log the response to the console
  } catch (error) {
    console.error(error);
  }
}

main();
