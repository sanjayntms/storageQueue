## Azure Storage Queue
   Azure Storage Queue is a robust and cost-effective messaging service designed for asynchronous communication between different components of cloud applications. It 
   acts as a buffer, allowing components to send and receive messages reliably, regardless of whether other components are simultaneously active.
*   Decoupling Applications: By using queues, you can separate application components, allowing them to scale and fail independently. For example, a web server that 
    receives user requests can enqueue them, and separate worker roles can process these requests in the background. This prevents the web server from being 
    overwhelmed during peak loads and improves the overall responsiveness of the application.  
*   Asynchronous Task Processing: Long-running or resource-intensive tasks can be offloaded to a queue for background processing. For instance, when a user uploads an 
    image, the web application can enqueue a message containing the image details. A separate worker role can then retrieve this message and perform tasks like 
    resizing, watermarking, or analysis without blocking the user's immediate interaction with the application.
** Key Features of Azure Storage Queue
* Scalability: Azure Storage Queues can handle a massive number of messages, scaling automatically to meet the demands of your application. A single queue can contain * millions of messages, limited only by the total capacity of the storage account (which is very large).
* Durability and Reliability: Messages in Azure Storage Queues are persistently stored, ensuring that they are not lost even if there are failures in other parts of 
  the system.
* Cost-Effective: Azure Storage Queues are a cost-efficient messaging solution, as you only pay for the storage you consume and the number of transactions you perform.
* Simple REST-based API: Interaction with the queue is done through a simple and well-documented REST API over HTTP/HTTPS, making it easy to use from various clients. 
* Visibility Timeout: When a consumer retrieves a message from the queue, it becomes temporarily invisible to other consumers for a specified duration (visibility 
  timeout). This prevents multiple consumers from processing the same message simultaneously. If the consumer fails to process the message within the timeout, it 
  becomes visible again for another consumer to pick up.   
* Message Size: Each message in an Azure Storage Queue can be up to 64 KB in size. For larger payloads, you can store the actual data in Azure Blob Storage and put a 
  reference to the blob in the queue message.   
* Message Time-to-Live (TTL): You can specify how long a message should remain in the queue before it expires and is automatically deleted.   
* Poison Message Handling: While not a direct feature, the dequeue count of a message is incremented each time it's retrieved. You can use this to identify and handle "poison messages" that repeatedly fail to process.   
** Benefits of Using Azure Storage Queue
* Improved Application Responsiveness: By offloading tasks to asynchronous processing via queues, front-end applications remain responsive to user interactions.   
* Increased System Reliability: The decoupling of components through queues makes the overall system more resilient to failures.   
* Enhanced Scalability: Queues enable applications to handle fluctuating loads by buffering requests and allowing background processes to scale independently.   
* Cost Optimization: The pay-as-you-go model of Azure Storage Queues helps optimize costs by only charging for actual usage.   
* Simplified Application Architecture: Queues provide a straightforward way to implement asynchronous communication patterns, simplifying the design of distributed 
  systems.   
* Easy Integration: Azure Storage Queues integrate seamlessly with other Azure services, making it easier to build complex cloud solutions.   

## In summary, Azure Storage Queue is a versatile and valuable service for building scalable, reliable, and efficient cloud applications that require asynchronous communication and task processing.


# Create Linux VM
 *  Cpoy app.py and worker.py (On same vm or you can deploy two VM)
 *  Create folder templates and copy index.html, upload_success.html
 *  Open port 3000 in NSG
 *  Create storage account and check app.py for blobs and queue containers.
 *  Export AZURE_STORAGE_CONNECTION_STRING="your_azure_storage_connection_string"
