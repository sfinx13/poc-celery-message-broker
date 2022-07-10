from service.convert_service import ConvertNumberService


convert_service = ConvertNumberService()
number_to_words = convert_service.to_words(500)
number_to_dollars = convert_service.to_dollars(5632)

print("number_to_words: {}".format(number_to_words))
print("number_to_dollars: {}".format(number_to_dollars))
