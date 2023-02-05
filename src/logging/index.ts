import { APIGatewayProxyEvent, Context } from 'aws-lambda'

let event: APIGatewayProxyEvent
let context: Context

export const setupLog = (
  awsEvent: APIGatewayProxyEvent,
  awsContext: Context
) => {
  event = awsEvent
  context = awsContext
}

export const log = (message = '') => {
  const { awsRequestId } = context

  console.log(
    JSON.stringify(
      {
        requestId: awsRequestId,
        datetime: new Date().toISOString(),
        message
      },
      null,
      2
    )
  )
}
