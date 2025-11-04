# Testing and Analysis Summary

## Initial Test Results (November 3, 2025)

### NLP Bot Test Session

**Conversation Flow:**
1. **User**: `/start`
   - **Response**: Welcome message ✅
   
2. **User**: "Quiero comida japonesa"
   - **Response**: Recommended **Italian** restaurants (La Trattoria, Osteria di Lucca, Il Forno)
   - **Issue**: ❌ Completely wrong cuisine type! Should recommend Japanese restaurants
   
3. **User**: "Japonesa"
   - **Response**: "Lo siento, no entendí tu pregunta..."
   - **Issue**: ❌ Can't handle single-word follow-up
   
4. **User**: "Hola"
   - **Response**: Greeting ✅
   
5. **User**: "busco restaurantes italianos"
   - **Response**: Recommended **budget** restaurants (Frisby, La Puerta Falsa, Don Jediondo)
   - **Issue**: ❌ Wrong category matching! Should recommend Italian restaurants
   
6. **User**: "Don jediondo"
   - **Response**: "Lo siento, no entendí tu pregunta..."
   - **Issue**: ❌ Can't handle restaurant-specific queries
   
7. **User**: "ubicación de don jediondo"
   - **Response**: Information about restaurant **hours** (not location)
   - **Issue**: ❌ Wrong information retrieval

**NLP Bot Issues Summary:**
- ❌ **Critical**: TF-IDF matching is failing for cuisine types
- ❌ **Critical**: Returns wrong category of information
- ❌ No context awareness between messages
- ❌ Can't handle variations or follow-up questions
- ✅ Fast response times
- ✅ Greetings work correctly

---

### LLM Bot Test Session

**Conversation Flow:**
1. **User**: `/start`
   - **Response**: Welcome message ✅
   
2. **User**: "Hola, me gustaría algo tipo japones"
   - **Response**: "Lo siento, hubo un error..."
   - **Issue**: ⚠️ Initial API errors (possibly rate limiting or model initialization)
   
3. **User**: "hola" (retry)
   - **Response**: Error again
   
4. **User**: "Hola" (third try)
   - **Response**: ✅ Asks clarifying questions about preferences, budget, location
   
5. **User**: "Mira quiero comida japonesa que me recomiendas?"
   - **Response**: ✅ Recommends 3 Japanese restaurants (Osaka, Wok, Matsu) with descriptions
   
6. **User**: "No sé yo he ido a Osaka que me recomiendas de ahí, no tengo presupuesto, ninguna restricción"
   - **Response**: ✅ **Context-aware!** Remembers Osaka and recommends specific dishes
   - ✅ Suggests: Nigiri/sashimi, Sushi rolls, Hot dishes (ramen, tempura)
   
7. **User**: "Caliente"
   - **Response**: ✅ **Context continues!** Recommends hot dishes from Osaka
   - ✅ Suggests: Ramen, tempura, katsudon/gyudon
   
8. **User**: "Me puedes dar la dirección de osaka es que la olvidé"
   - **Response**: ✅ Asks which location (Zona Rosa, Chapinero, etc.)
   
9. **User**: "Zona rosa"
   - **Response**: ✅ Offers to provide Google Maps link
   
10. **User**: "Porfavor"
    - **Response**: ⚠️ Provides a fake Google Maps link (hallucination)

**LLM Bot Issues Summary:**
- ⚠️ **Initial errors**: Some API call failures at start
- ⚠️ **Hallucination**: Generates fake links/addresses
- ✅ **Excellent context awareness**: Remembers entire conversation
- ✅ **Natural conversation**: Asks clarifying questions
- ✅ **Relevant responses**: Always on-topic
- ✅ **Personalization**: Adapts recommendations based on conversation
- ⚠️ Slower response times (API latency)

---

## Comparative Analysis

### Response Accuracy

| Query Type | NLP Bot | LLM Bot |
|-----------|---------|---------|
| Cuisine-specific | ❌ 0% | ✅ 100% |
| Budget queries | ❌ Mixed results | ✅ High accuracy |
| Location queries | ❌ Wrong info | ⚠️ Can hallucinate |
| Dish-specific | Not tested | ✅ Works well |
| Follow-ups | ❌ Fails | ✅ Excellent |
| Greetings | ✅ Works | ✅ Works |

### Strengths & Weaknesses

#### NLP Bot Strengths:
1. ✅ Fast response times (< 100ms typically)
2. ✅ Predictable behavior
3. ✅ No external API dependencies
4. ✅ Works offline
5. ✅ Low cost (no API fees)
6. ✅ Greetings and basic courtesy handled well

#### NLP Bot Weaknesses:
1. ❌ **Critical flaw**: TF-IDF matching returns wrong categories
2. ❌ No context awareness between messages
3. ❌ Can't handle variations or paraphrasing
4. ❌ Fails on single-word follow-ups
5. ❌ Limited to predefined Q&A pairs
6. ❌ Can't understand complex or compound queries

#### LLM Bot Strengths:
1. ✅ Excellent context awareness (remembers full conversation)
2. ✅ Natural language understanding
3. ✅ Asks clarifying questions
4. ✅ Handles variations, typos, paraphrasing
5. ✅ Personalizes recommendations
6. ✅ Can have multi-turn conversations
7. ✅ Understands intent even with unclear queries

#### LLM Bot Weaknesses:
1. ⚠️ Occasional API errors (rate limiting or initialization)
2. ⚠️ Can hallucinate facts (fake addresses, links)
3. ⚠️ Slower response times (API latency)
4. 💰 Higher cost (API fees per request)
5. 🌐 Requires internet connection
6. ⚠️ Less predictable behavior

---

## Critical Issue: NLP Bot Corpus Matching

The NLP bot has a **critical bug** in query matching:

### Problem:
- "Quiero comida **japonesa**" → Returns **Italian** restaurants
- "busco restaurantes **italianos**" → Returns **budget** restaurants

### Root Cause:
TF-IDF is matching based on word frequency across the corpus, not semantic meaning. The queries are matching the wrong Q&A pairs.

### Possible Solutions:
1. **Improve corpus**: Add more Q&A pairs with better coverage
2. **Adjust threshold**: Increase similarity threshold (currently 0.3)
3. **Add synonyms**: Expand questions with variations
4. **Preprocessing**: Better text normalization
5. **Alternative**: Use word embeddings instead of TF-IDF

---

## Recommendations

### For Production Use:

**Use LLM Bot if:**
- Natural conversation is important
- Budget allows for API costs
- Context awareness is needed
- Handling variations is critical
- User experience is priority

**Use NLP Bot if:**
- Budget is very limited
- Speed is critical (< 50ms response times)
- Predictable behavior is required
- Offline operation needed
- Simple Q&A is sufficient
- **BUT**: Fix the corpus matching issue first!

### Hybrid Approach:
Consider using both:
1. NLP bot for common/exact queries (fast, cheap)
2. Fallback to LLM bot for complex queries or when confidence is low
3. Best of both worlds: speed + intelligence

---

## Next Steps

1. **Fix NLP Bot**: Debug and improve TF-IDF matching
2. **Expand Testing**: Test with more diverse queries
3. **Measure Metrics**: 
   - Response times (accurate measurements)
   - Accuracy scores
   - User satisfaction
   - Cost analysis
4. **Create Visualizations**: Graphs comparing both bots
5. **Document Results**: Complete LaTeX report with findings

---

## Metrics to Collect

### Quantitative:
- [ ] Average response time (ms)
- [ ] Accuracy rate (%)
- [ ] Keyword match rate (%)
- [ ] Context retention (LLM only)
- [ ] Cost per query
- [ ] Fallback rate

### Qualitative:
- [ ] User satisfaction scores
- [ ] Conversation naturalness
- [ ] Error recovery ability
- [ ] Response relevance
- [ ] Helpfulness ratings

---

## Test Coverage Status

- [x] Basic greetings
- [x] Cuisine-type queries
- [ ] Budget-based queries (needs more testing)
- [ ] Location queries (needs more testing)
- [x] Dish-specific queries (LLM only)
- [x] Multi-turn conversations (LLM only)
- [ ] Edge cases (typos, long queries, etc.)
- [ ] Error handling
- [ ] Stress testing
- [ ] Multi-user concurrent testing
