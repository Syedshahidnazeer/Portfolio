def get_projects(role):
    """Returns a dictionary of projects based on the selected role."""
    if role == "Data Analyst":
        projects = {
            "Sales Dashboard Creation": """
            - **Project Overview:** Imagine a symphony of sales data—revenue notes, customer crescendos, and profit harmonies. That’s what our Sales Dashboard Creation is all about.
            - **The Challenge:** Our sales team needed a compass—a dashboard that would guide them through the labyrinth of metrics. Enter Power BI, our maestro.
            - **The Crescendo:** We composed interactive dashboards that danced with KPIs: revenue trends pirouetting, conversion rates waltzing, and customer churn doing the cha-cha.
            - **The Encore:** Efficiency soared by 15%, like a soprano hitting a high note. Our sales team? They became virtuosos, armed with insights and ready to conquer markets.
            """,
            "Customer Segmentation Analysis": """
            - **Project Prelude:** Picture a kaleidoscope of customer data—purchase histories, demographics, and behavioral quirks. Our mission? Unravel the patterns.
            - **The Clusters:** We donned our Sherlock hats and performed cluster analysis. Voilà! Customer segments emerged: the Loyal Larks, the Bargain Hunters, and the Impulse Buyers.
            - **The Marketing Sonata:** Armed with insights, marketing campaigns became laser-focused. Personalized emails serenaded the Loyal Larks, while flash sales beckoned the Impulse Buyers.
            - **The Standing Ovation:** Customer retention swirled like a waltz—up by 10%. The audience (read: stakeholders) cheered. Encore, please!
            """,
            "Supply Chain Optimization": """
            - **Project Prelude (in Minor Key):** Our supply chain resembled rush hour traffic—bottlenecks, detours, and missed deliveries. Chaos reigned.
            - **The Data Expedition:** Armed with logistics data, we embarked on a quest. Our goal? Efficiency nirvana.
            - **The Hidden Paths:** We analyzed routes, inventory levels, and lead times. Inefficiencies trembled. Bottlenecks quivered.
            - **The Symphony of Savings:** Logistics costs bowed out gracefully—down by 8%. Our supply chain? Now a well-choreographed ballet, pirouetting toward cost-effectiveness.
            """
        }
    elif role == "Data Scientist":
        projects = {
            "Rating Prediction of Google Play Store Apps Using Data Mining Techniques": """
            - **Project Prelude (in Data Science Symphony):** Imagine a bustling app store, a sea of apps vying for attention. Developers struggle to understand what makes an app soar to the top, or why some crash and burn.  Our mission?  Unlock the secrets of app success using data.
            - **The Algorithm's Maestro:** We donned our data scientist hats and conducted a symphony of data mining. Over 100,000 apps, their reviews, features, and categories, became our musical score.  We trained our algorithms on this vast orchestra of data, seeking the hidden patterns that predict app success.
            - **The Rating's Crescendo:**  Our model, like a maestro conducting an orchestra, predicted app ratings with 93% accuracy. Developers, armed with this knowledge, could now compose apps that resonated with users. It was a concerto of data-driven app development, leading to increased downloads and higher rankings.
            - **The Standing Ovation:** The app store's stage was now illuminated by data-driven decisions, as developers composed apps that captivated users, achieving greater success and making the app store a truly harmonious experience.
            """,
            "Real-Time News Verification Web App": """
            - **Project Prelude (in Digital Journalism's Dilemma):**  Picture a world awash in information, but where truth is increasingly elusive.  Fake news spreads like wildfire, leaving people confused and questioning reality. Our mission?  To build a beacon of truth in a digital sea of misinformation.
            - **The NLP's Sleuth:**  We crafted a web app powered by advanced NLP, trained on over 80,000 articles. It became our digital detective, analyzing the language of news stories, seeking inconsistencies and identifying telltale signs of fakery.
            - **The Verification Tango:** This web app, like a swift and accurate dance, could verify the authenticity of news within milliseconds.  It eliminated the time-consuming and often inaccurate manual verification process, empowering users to trust the news they consume.
            - **The Spotlight on Truth:**  Our app became a spotlight, shining brightly on the truth in a world saturated with misinformation.  Users could now confidently navigate the digital landscape, knowing they had access to reliable and verified news.
            """,
            "Oil Price Prediction Application": """
            - **Project Prelude (in Energy Market's Volatility):**  Imagine a global market where the price of oil can fluctuate wildly, throwing businesses and economies into turmoil.  Our mission?  To tame the chaos and bring predictability to the oil industry.
            - **The Data's Oracle:**  We delved into over 35 years of historical oil price data, a vast collection of numbers representing the ebb and flow of the energy market. We trained our predictive models on this vast dataset, seeking the patterns that could unlock the secrets of oil price fluctuations.
            - **The Prediction's Compass:** Our application, like a skilled navigator charting the course through stormy seas, provided oil price forecasts with a prediction variance of just 1.2% to 2%. This gave businesses and investors a valuable tool for strategic planning and decision-making in the volatile oil market.
            - **The Oil Industry's Stability:** The oil industry, once plagued by unpredictable price swings, now had a valuable tool to navigate the market effectively. Our app brought stability and confidence to an industry that had long faced volatility, enabling better decision-making and fostering growth. 
            """
        }
    else:  # Python Developer
        projects = {
            "E-commerce Platform Development": """
            - **Project Prelude:** Imagine an online marketplace—the hustle, the clicks, the virtual cash registers ringing. Our mission? To build a platform that could handle the shopping frenzy.
            - **The Django Symphony:** We donned our developer capes and danced with Django. Scalability was our muse, and we crafted an e-commerce wonderland. Product listings pirouetted, carts cha-chaed, and checkout flows waltzed.
            - **The Sales Crescendo:** Online sales soared—up by 50%. Customers clicked, bought, and left with virtual shopping bags full of joy. Our platform? The grand stage for this retail ballet.
            """,
            "API Integration Service": """
            - **Project Prelude (in Microservice Notes):** Picture a data orchestra—each service playing its part, harmonizing like well-tuned instruments. But what if these services spoke different languages? Chaos, my friend.
            - **The Polyglot Maestro:** We composed a microservice-based API integration platform. REST, GraphQL, SOAP—they all bowed to our conductor. Data flowed seamlessly, like a symphony in sync.
            - **The Tempo Accelerando:** Data processing time? Reduced by 60%. Our platform? The bridge connecting disparate systems. APIs high-fived, and business logic danced a jig.
            """,
            "Automated Testing Framework": """
            - **Project Prelude (in Code Coverage Notes):** Imagine a codebase—the notes, the harmonies, the occasional dissonance (read: bugs). Our mission? To ensure every note played true.
            - **The Testing Sonata:** We composed a comprehensive testing framework. Unit tests, integration tests, end-to-end tests—they swirled like musical motifs. Code coverage climbed, bugs trembled.
            - **The Bug-Free Finale:** Bug reports? Down by 30%. Our framework? The vigilant conductor, ensuring every line of code sang its best. Developers smiled, users hummed along.
            """
        }
    return projects